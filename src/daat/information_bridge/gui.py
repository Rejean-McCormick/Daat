"""DaaT Studio: offline, no console, multi-source context preparation UI.

The GUI does not authenticate access or transmit material to ChatGPT. Every
permission is an explicit operator declaration, not an owner-issued grant.
"""
from __future__ import annotations
from pathlib import Path
from queue import Empty,Queue
from threading import Thread,Event
import json
import os
import tkinter as tk
from tkinter import ttk,filedialog,messagebox

from .cli import build_from_data,build_from_job
from .model import BridgeError
from .registry import SourceRegistry, AccessPlanner
from .diagnostic import readiness
from .context import verify_export
from .ai_review import validate_response, correction_prompt, response_template, save_review

_ACTIONS=('read','copy','retain','transform','ai_disclosure')
_KINDS=('reference_only','abstract','excerpt','full_text_authorized','structured_record','dataset','media_derivative')

class Studio:
    def __init__(self,root:tk.Tk):
        self.root=root; root.title('DaaT Studio — pont universel d’information')
        root.geometry('1060x780');root.minsize(850,630)
        self.registry=SourceRegistry()
        self.sources=[]
        self.queue=Queue();self.running=False;self.cancel=Event();self.last_export=None
        self.last_correction_prompt=""
        self.last_review_response=None
        self.status=tk.StringVar(value='Prêt. Aucun accès réseau ni envoi ChatGPT automatique.')
        self.progress=tk.DoubleVar(value=0.0)
        self.question=tk.StringVar(value='Que peut-on établir à partir des sources réellement disponibles?')
        self.input_root=tk.StringVar(value=str(Path.home()))
        self.output_root=tk.StringVar(value=str(Path.home()))
        self.platform=tk.StringVar(value='medium')
        self.title=tk.StringVar();self.author=tk.StringVar()
        self.external=tk.StringVar();self.revision=tk.StringVar(value='user-snapshot-1')
        self.kind=tk.StringVar(value='excerpt')
        self.access=tk.StringVar(value='fichier')
        self.file=tk.StringVar()
        self.basis=tk.StringVar()
        self.evidence=tk.StringVar()
        self.classification=tk.StringVar(value='public')
        self.consent={action:tk.BooleanVar(value=False) for action in _ACTIONS}
        self._build()
        self.root.after(100,self.poll)

    def _build(self):
        main=ttk.Frame(self.root,padding=12);main.pack(fill='both',expand=True)
        ttk.Label(main,text='DaaT Studio',font=('Segoe UI',19,'bold')).pack(anchor='w')
        ttk.Label(main,text='Préparation contrôlée d’un contexte ChatGPT — aucun Kristal, aucune récupération de session.',
                  foreground='#666').pack(anchor='w',pady=(0,7))
        nb=ttk.Notebook(main);nb.pack(fill='both',expand=True)
        add=ttk.Frame(nb,padding=12);project=ttk.Frame(nb,padding=12);catalog=ttk.Frame(nb,padding=12);review=ttk.Frame(nb,padding=12)
        nb.add(add,text='1. Sources');nb.add(project,text='2. Dossier ChatGPT');nb.add(review,text='3. Réponse ChatGPT');nb.add(catalog,text='4. Registre et diagnostics')
        self._sources_tab(add);self._project_tab(project);self._review_tab(review);self._catalog_tab(catalog)
        foot=ttk.Frame(main);foot.pack(fill='x',pady=(10,0))
        ttk.Progressbar(foot,variable=self.progress,maximum=100).pack(fill='x',pady=4)
        ttk.Label(foot,textvariable=self.status).pack(anchor='w')

    def _row(self,parent,label,value,width=25):
        fr=ttk.Frame(parent);fr.pack(fill='x',pady=3)
        ttk.Label(fr,text=label,width=width).pack(side='left')
        ent=ttk.Entry(fr,textvariable=value);ent.pack(side='left',fill='x',expand=True)
        return fr

    def _sources_tab(self,parent):
        top=ttk.LabelFrame(parent,text='Décrire une source réellement accessible',padding=8)
        top.pack(fill='x')
        line=ttk.Frame(top);line.pack(fill='x',pady=3)
        ttk.Label(line,text='Plateforme',width=25).pack(side='left')
        values=sorted(self.registry.profiles)
        ttk.Combobox(line,textvariable=self.platform,values=values,width=35).pack(side='left')
        ttk.Label(line,text='Portée',padding=(18,0,3,0)).pack(side='left')
        ttk.Combobox(line,textvariable=self.kind,values=_KINDS,width=24,state='readonly').pack(side='left')
        self._row(top,'Titre (facultatif)',self.title)
        self._row(top,'Auteur (facultatif)',self.author)
        self._row(top,'ID / référence externe',self.external)
        self._row(top,'Révision / instantané',self.revision)
        select=ttk.Frame(top);select.pack(fill='x',pady=3)
        ttk.Label(select,text='Contenu',width=25).pack(side='left')
        ttk.Combobox(select,textvariable=self.access,values=('fichier','collage','référence seule'),
                     width=22,state='readonly').pack(side='left')
        ttk.Entry(select,textvariable=self.file).pack(side='left',fill='x',expand=True,padx=5)
        ttk.Button(select,text='Parcourir',command=self.choose_source_file).pack(side='left')
        ttk.Label(top,text='Texte à coller (uniquement si « collage ») :').pack(anchor='w',pady=(4,1))
        self.paste=tk.Text(top,height=4,wrap='word');self.paste.pack(fill='x')
        rights=ttk.LabelFrame(parent,text='Déclaration explicite des droits — un login ne suffit pas',padding=8)
        rights.pack(fill='x',pady=8)
        perms=ttk.Frame(rights);perms.pack(fill='x')
        labels={'read':'Lire','copy':'Copier','retain':'Conserver dans le dossier','transform':'Transformer',
                'ai_disclosure':'Transmettre à ChatGPT'}
        for action in _ACTIONS:
            ttk.Checkbutton(perms,text=labels[action],variable=self.consent[action]).pack(side='left',padx=6)
        self._row(rights,'Base de l’autorisation',self.basis)
        self._row(rights,'Référence de preuve non secrète',self.evidence)
        line=ttk.Frame(rights);line.pack(anchor='w')
        ttk.Label(line,text='Classification',width=25).pack(side='left')
        ttk.Combobox(line,textvariable=self.classification,values=('public','internal','confidential','restricted'),
                     state='readonly',width=23).pack(side='left')
        ttk.Label(rights,text='Cette déclaration est fournie par l’opérateur; elle ne remplace pas une autorisation du fournisseur.',
                  foreground='#875b00').pack(anchor='w',pady=3)
        add_buttons=ttk.Frame(parent);add_buttons.pack(anchor='w')
        ttk.Button(add_buttons,text='Ajouter cette source au lot',command=self.add_source).pack(side='left',padx=(0,10))
        ttk.Button(add_buttons,text='Ajouter plusieurs fichiers (un seul lot)',command=self.add_multiple_files).pack(side='left')
        self.table=ttk.Treeview(parent,columns=('platform','kind','access','rights'),show='headings',height=5)
        for col,width in [('platform',135),('kind',190),('access',180),('rights',185)]:
            self.table.heading(col,text=col);self.table.column(col,width=width)
        self.table.pack(fill='both',expand=True,pady=(8,3))
        ttk.Button(parent,text='Supprimer la sélection',command=self.remove_source).pack(anchor='w')

    def _project_tab(self,parent):
        form=ttk.LabelFrame(parent,text='Projet / demande de contexte',padding=12);form.pack(fill='x')
        self._row(form,'Question pour ChatGPT',self.question)
        folder=self._row(form,'Dossier racine des fichiers',self.input_root)
        ttk.Button(folder,text='Choisir',command=lambda:self.choose_dir(self.input_root)).pack(side='left')
        out=self._row(form,'Dossier des exports',self.output_root)
        ttk.Button(out,text='Choisir',command=lambda:self.choose_dir(self.output_root)).pack(side='left')
        ttk.Label(form,text='La sortie sera créée dans un NOUVEAU sous-dossier. Aucun contenu n’est envoyé automatiquement.',
                  foreground='#666').pack(anchor='w',pady=4)
        buttons=ttk.Frame(parent);buttons.pack(fill='x',pady=10)
        self.run_btn=ttk.Button(buttons,text='Construire le dossier contextuel',command=self.start)
        self.run_btn.pack(side='left',padx=4)
        ttk.Button(buttons,text='Annuler',command=self.cancel_work).pack(side='left',padx=4)
        ttk.Button(buttons,text='Ouvrir le prompt',command=self.open_prompt).pack(side='left',padx=4)
        ttk.Button(buttons,text='Vérifier le dernier export',command=self.verify).pack(side='left',padx=4)
        self.log=tk.Text(parent,height=19,wrap='word',state='disabled')
        self.log.pack(fill='both',expand=True)
        ttk.Label(parent,text='Important : l’export est préparé et non transmis; la revue des droits et citations reste obligatoire.',
                  foreground='#666').pack(anchor='w',pady=5)

    def _review_tab(self,parent):
        ttk.Label(parent,text='Colle ici la réponse JSON de ChatGPT. Les citations sont vérifiées mot pour mot.',
                  foreground='#555').pack(anchor='w',pady=5)
        self.response=tk.Text(parent,height=13,wrap='word');self.response.pack(fill='both',expand=True)
        controls=ttk.Frame(parent);controls.pack(fill='x',pady=7)
        ttk.Button(controls,text='Vérifier la réponse',command=self.check_response).pack(side='left',padx=4)
        ttk.Button(controls,text='Copier le format JSON attendu',command=self.copy_response_template).pack(side='left',padx=4)
        ttk.Button(controls,text='Copier le prompt de correction',command=self.copy_correction).pack(side='left',padx=4)
        ttk.Button(controls,text='Exporter la revue',command=self.export_review).pack(side='left',padx=4)
        ttk.Label(parent,text='Résultat local (ne confirme pas la vérité des assertions ni une autorité canonique) :').pack(anchor='w')
        self.review_log=tk.Text(parent,height=12,wrap='word',state='disabled')
        self.review_log.pack(fill='both',expand=True)

    def _current_bundle(self):
        if self.last_export is None:
            raise BridgeError('NO_EXPORT','Construire et vérifier un dossier ChatGPT avant cette opération.')
        verify_export(self.last_export)
        return json.loads((self.last_export/'context-bundle.json').read_text(encoding='utf-8'))

    def copy_response_template(self):
        try:
            template=response_template(self._current_bundle())
        except (BridgeError,ValueError,OSError) as exc:
            messagebox.showwarning('Dossier requis',getattr(exc,'code','INVALID_EXPORT'));return
        self.root.clipboard_clear();self.root.clipboard_append(template)
        self._write_text(self.review_log,'Format JSON copié. Il ne contient aucune source additionnelle.')

    def copy_correction(self):
        if not self.last_correction_prompt:
            messagebox.showinfo('Correction','Aucun refus de réponse à corriger.');return
        self.root.clipboard_clear();self.root.clipboard_append(self.last_correction_prompt)
        self._write_text(self.review_log,'Consigne de correction copiée pour ChatGPT.')

    def export_review(self):
        if self.last_review_response is None:
            messagebox.showinfo('Revue','Valider une réponse JSON avant d’exporter sa revue.');return
        try:
            folder=filedialog.askdirectory(title='Choisir le dossier parent du rapport de revue')
            if not folder:return
            import datetime
            unique='DaaT_Revue_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            result=save_review(self._current_bundle(),self.last_review_response,Path(folder)/unique)
            self._write_text(self.review_log,'Revue non canonique exportée : '+result['saved_to'])
        except (BridgeError,ValueError,OSError) as exc:
            messagebox.showwarning('Export de revue refusé',getattr(exc,'code','REVIEW_ERROR'))

    def check_response(self):
        try:
            bundle=self._current_bundle()
            raw=self.response.get('1.0','end-1c').strip()
            if len(raw)>1_000_000:
                raise BridgeError('AI_LIMIT','Réponse JSON trop volumineuse.')
            if raw.startswith('```') and raw.endswith('```'):
                raw=raw.split('\n',1)[-1].rsplit('```',1)[0].strip()
            response=json.loads(raw)
            result=validate_response(bundle,response)
            self.last_review_response=response
            self.last_correction_prompt=''
            self._write_text(self.review_log,
                'Citations présentes, structure valide; '+str(len(result['items']))+
                ' proposition(s) NON fiables en attente de revue humaine.',clear=True)
        except (BridgeError,ValueError,KeyError,TypeError,OSError) as exc:
            self.last_review_response=None
            code=getattr(exc,'code','AI_JSON_INVALID')
            bundle_id='dossier courant'
            try:bundle_id=self._current_bundle()['manifest']['bundle_id']
            except (BridgeError,ValueError,OSError,KeyError):pass
            self.last_correction_prompt=correction_prompt(exc,bundle_id)
            self._write_text(self.review_log,
                 'REFUS : '+code+' — aucune proposition acceptée. Utiliser « Copier le prompt de correction ».',clear=True)

    def _catalog_tab(self,parent):
        self.search=tk.StringVar()
        searchrow=self._row(parent,'Rechercher parmi 89 profils',self.search)
        ttk.Button(searchrow,text='Rechercher',command=self.search_platforms).pack(side='left')
        ttk.Button(parent,text='Diagnostic de couverture locale',command=self.show_diagnostic).pack(anchor='w',pady=4)
        self.catalog_text=tk.Text(parent,height=25,wrap='word',state='disabled')
        self.catalog_text.pack(fill='both',expand=True)
        self.search_platforms()

    def _write_text(self,widget,message,clear=False):
        widget.configure(state='normal')
        if clear:widget.delete('1.0','end')
        widget.insert('end',message+'\n');widget.see('end');widget.configure(state='disabled')
    def log_note(self,message):self._write_text(self.log,message)
    def choose_dir(self,var):
        path=filedialog.askdirectory()
        if path:var.set(path)
    def choose_source_file(self):
        value=filedialog.askopenfilename()
        if value:
            path=Path(value)
            root=Path(self.input_root.get())
            try:rel=path.relative_to(root)
            except ValueError:
                self.input_root.set(str(path.parent)); rel=Path(path.name)
            self.file.set(str(rel));self.access.set('fichier')
    def add_source(self):
        try:
            platform=self.platform.get().strip();self.registry.get(platform)
            mode=self.access.get();kind=self.kind.get()
            if mode=='référence seule':kind='reference_only'
            if kind=='reference_only' and mode!='référence seule':
                raise ValueError('Pour reference_only, choisir « référence seule ».')
            user_ref=self.external.get().strip()
            if not user_ref:raise ValueError('Indiquer un identifiant externe (URL, DOI, numéro de document, etc.).')
            basis=self.basis.get().strip();evidence=self.evidence.get().strip()
            permitted={a:('allowed' if self.consent[a].get() else 'unknown') for a in _ACTIONS}
            if any(v=='allowed' for v in permitted.values()) and (not basis or not evidence):
                raise ValueError('Les permissions cochées exigent une base et une référence de preuve sans secret.')
            rights={**permitted,'basis':basis,'evidence_ref':evidence,
                    'attestation':'operator_asserted' if any(self.consent[a].get() for a in _ACTIONS) else 'unverified',
                    'classification':self.classification.get()}
            obj={'platform_id':platform,'external_id':user_ref,'revision':self.revision.get().strip(),
                 'title':self.title.get().strip(),'author':self.author.get().strip(),
                 'content_kind':kind,'rights':rights,
                 'acquired_via':{'fichier':'user_export','collage':'user_paste','référence seule':'federated_ref'}[mode]}
            if mode=='fichier':
                if not self.file.get().strip():raise ValueError('Choisir un fichier situé dans le dossier racine.')
                obj['path']=self.file.get().strip()
            elif mode=='collage':
                value=self.paste.get('1.0','end-1c')
                if not value.strip():raise ValueError('Le texte à coller est vide.')
                obj['text']=value
            self.sources.append(obj)
            self.table.insert('', 'end',values=(platform,kind,mode,
                  '5/5 permissions' if all(self.consent[a].get() for a in _ACTIONS) else 'partiel / inconnu'))
            self.status.set(f'{len(self.sources)} sources sélectionnées.')
            self.paste.delete('1.0','end');self.file.set('');self.external.set('')
        except (ValueError,KeyError) as exc:
            messagebox.showerror('Source invalide',str(exc))
    def add_multiple_files(self):
        """One explicit operator-rights declaration for a selected batch of local files.

        This never claims the files were granted by their remote source. Every
        file is still parsed and checked individually by LocalIngestor.
        """
        try:
            platform=self.platform.get().strip();self.registry.get(platform)
            kind=self.kind.get()
            if kind=='reference_only':
                raise ValueError('Choisir une portée autre que « référence seule » pour des fichiers.')
            basis=self.basis.get().strip();evidence=self.evidence.get().strip()
            permitted={a:('allowed' if self.consent[a].get() else 'unknown') for a in _ACTIONS}
            if any(v=='allowed' for v in permitted.values()) and (not basis or not evidence):
                raise ValueError('Permissions : préciser la base et la référence de preuve.')
            paths=[Path(x) for x in filedialog.askopenfilenames(title='Choisir les fichiers autorisés du lot')]
            if not paths:return
            if len(paths)>500 or len(paths)+len(self.sources)>500:
                raise ValueError('Maximum 500 sources par lot : diviser le corpus.')
            parent=paths[0].parent
            if any(p.parent!=parent for p in paths):
                raise ValueError('Choisir des fichiers dans un même dossier pour un lot sécurisé.')
            self.input_root.set(str(parent))
            rights={**permitted,'basis':basis,'evidence_ref':evidence,
                    'attestation':'operator_asserted' if any(self.consent[a].get() for a in _ACTIONS) else 'unverified',
                    'classification':self.classification.get()}
            reference=self.external.get().strip()
            revision=self.revision.get().strip()
            if not revision:raise ValueError('Indiquer une révision / un instantané.')
            for path in paths:
                item={'platform_id':platform,'external_id':f'{reference or "local-batch"}/{path.name}',
                      'revision':revision,'title':self.title.get().strip() or path.stem,
                      'author':self.author.get().strip(),'content_kind':kind,
                      'rights':dict(rights),'acquired_via':'user_export','path':path.name}
                self.sources.append(item)
                self.table.insert('', 'end',values=(platform,kind,'fichier: '+path.name,
                    '5/5 permissions' if all(self.consent[a].get() for a in _ACTIONS) else 'partiel / inconnu'))
            self.status.set(f'{len(self.sources)} sources sélectionnées (lot ajouté : {len(paths)}).')
        except (ValueError,KeyError) as exc:
            messagebox.showerror('Lot de fichiers invalide',str(exc))

    def remove_source(self):
        selections=self.table.selection()
        indexes=sorted((self.table.index(item) for item in selections),reverse=True)
        for index in indexes:
            self.sources.pop(index)
            item=self.table.get_children()[index]
            self.table.delete(item)
        self.status.set(f'{len(self.sources)} sources sélectionnées.')

    def start(self):
        if self.running:return
        if not self.sources:
            messagebox.showwarning('Aucune source','Ajouter au moins une source dans le premier onglet.');return
        if not self.question.get().strip():
            messagebox.showwarning('Question requise','Définir une question pour ChatGPT.');return
        self.cancel.clear()
        self.running=True;self.run_btn.configure(state='disabled');self.progress.set(0)
        job={'question':self.question.get().strip(),'language':'fr','sources':[dict(s) for s in self.sources]}
        root=Path(self.input_root.get());out_root=Path(self.output_root.get())
        import datetime
        folder='DaaT_Context_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        output=out_root/folder
        self.status.set('Préparation en cours…');self.log_note('Lecture du lot : aucune requête réseau.')
        def progress(i,total,ref):
            if self.cancel.is_set():raise BridgeError('CANCELLED','Cancelled by operator')
            self.queue.put(('progress',i,total,ref))
        def work():
            try:
                from .cli import build_from_data
                result=build_from_data(job,root,output,progress=progress)
                verified=verify_export(output)
                self.queue.put(('done',result,verified))
            except Exception as exc:
                self.queue.put(('error',getattr(exc,'code','BUILD_ERROR')))
        Thread(target=work,daemon=True).start()
    def cancel_work(self):
        if self.running:self.cancel.set();self.status.set('Annulation demandée…')
    def poll(self):
        try:
            while True:
                msg=self.queue.get_nowait()
                if msg[0]=='progress':
                    _,i,total,ref=msg
                    self.progress.set(i/total*100)
                    self.status.set(f'{i}/{total} sources examinées — {100*i/total:.0f}%')
                    self.log_note(f'[{i}/{total}] {ref} traité; droits évalués avant export.')
                elif msg[0]=='done':
                    self.running=False;self.run_btn.configure(state='normal')
                    r=msg[1];self.last_export=Path(r['export'])
                    self.progress.set(100);self.status.set('Dossier prêt pour revue humaine — non transmis')
                    self.log_note(f"Export vérifié: {r['export']}")
                    self.log_note(f"Sources: {r['sources']}; fragments: {r['fragments']}; exclusions: {r['excluded']}")
                elif msg[0]=='error':
                    self.running=False;self.run_btn.configure(state='normal')
                    self.status.set('Interrompu : '+msg[1]);self.log_note('Échec sûr: '+msg[1])
        except Empty:pass
        self.root.after(100,self.poll)
    def open_prompt(self):
        if self.last_export is None:return
        p=self.last_export/'prompt-chatgpt.md'
        if p.exists():
            if os.name=='nt':os.startfile(str(p))
            else:messagebox.showinfo('Fichier',str(p))
    def verify(self):
        if self.last_export is None:return
        try:res=verify_export(self.last_export)
        except Exception as exc:messagebox.showwarning('Non valide',getattr(exc,'code','VERIFY_ERROR'))
        else:messagebox.showinfo('Intégrité locale','Conforme (SHA-256 non signé).\n'+res['bundle_id'])
    def search_platforms(self):
        profiles=self.registry.search(self.search.get())
        lines=[]
        for p in profiles:
            lines.append(p['platform']+' ['+p['id']+']')
            lines.append('  Méthodes : '+', '.join(x['mode'] for x in p['access_paths']))
            lines.append('  Statut connecteur : '+p['daat_connector_status'])
            lines.append('  Autorisations : '+p['owner_authorization_status'])
            lines.append('')
        self._write_text(self.catalog_text,'\n'.join(lines) if lines else 'Aucun profil',clear=True)
    def show_diagnostic(self):
        data=readiness()
        status=data['registry']
        summary=(f"Couverture : {status['profiles']} profils, {status['families']} familles.\n"
                 f"Documentations officielles consultées : {status['official_docs_profiles']}.\n"
                 f"Non vérifiées : {status['unverified_docs_profiles']}.\n"
                 'Statut : NON QUALIFIÉ POUR PRODUCTION.\n'
                 'Aucun connecteur fournisseur n’est déclaré officiellement opérationnel par ce diagnostic.')
        self._write_text(self.catalog_text,summary,clear=True)

def main():
    root=tk.Tk();Studio(root);root.mainloop()

if __name__=='__main__':main()
