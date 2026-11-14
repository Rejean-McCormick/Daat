"""DaAT — Explorateur hors ligne des modes d'accès des plateformes.

Catalogue de recherche seulement. Aucune requête réseau et aucune connexion à un compte.
"""
from pathlib import Path
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

ROOT=Path(__file__).resolve().parent
REGISTRY=ROOT/'docs'/'data'/'platform-access-registry.v1.json'

class Browser:
    def __init__(self, top):
        self.top=top
        self.top.title('DaAT — Registre des sources (recherche v1)')
        self.top.geometry('1050x670')
        self.doc=json.loads(REGISTRY.read_text(encoding='utf-8'))
        self.records=self.doc['platforms']
        self.filtered=[]
        self.q=tk.StringVar()
        container=ttk.Frame(top,padding=12)
        container.pack(fill='both',expand=True)
        ttk.Label(container,text='DaAT — Explorer les accès aux sources',font=('Segoe UI',15,'bold')).pack(anchor='w')
        ttk.Label(container,text='89 profils · 36 familles · Catalogue hors ligne : aucun connecteur activé',foreground='#666666').pack(anchor='w',pady=(0,10))
        row=ttk.Frame(container)
        row.pack(fill='x',pady=(0,10))
        ttk.Label(row,text='Rechercher : ').pack(side='left')
        entry=ttk.Entry(row,textvariable=self.q)
        entry.pack(side='left',fill='x',expand=True)
        entry.focus()
        self.q.trace_add('write',lambda *_:self.refresh())
        split=ttk.Panedwindow(container,orient='horizontal')
        split.pack(fill='both',expand=True)
        left=ttk.Frame(split)
        right=ttk.Frame(split)
        split.add(left,weight=1)
        split.add(right,weight=3)
        self.lst=tk.Listbox(left,exportselection=False,font=('Segoe UI',10))
        y=ttk.Scrollbar(left,orient='vertical',command=self.lst.yview)
        self.lst.configure(yscrollcommand=y.set)
        self.lst.pack(side='left',fill='both',expand=True)
        y.pack(side='right',fill='y')
        self.lst.bind('<<ListboxSelect>>',lambda _:self.show())
        self.detail=scrolledtext.ScrolledText(right,wrap='word',font=('Consolas',10),state='disabled',padx=12,pady=10)
        self.detail.pack(fill='both',expand=True)
        foot=ttk.Frame(container)
        foot.pack(fill='x',pady=(10,0))
        ttk.Button(foot,text='Copier les détails',command=self.copy).pack(side='right')
        ttk.Label(foot,text='Aucun scraping, jeton, accès réseau ou publication',foreground='#666666').pack(side='left')
        self.refresh()

    def refresh(self):
        q=self.q.get().casefold().strip()
        self.filtered=[r for r in self.records if q in (r['platform']+' '+r['id']+' '+' '.join(r['family_labels'])).casefold()]
        self.lst.delete(0,'end')
        for r in self.filtered:self.lst.insert('end',r['platform'])
        if self.filtered:
            self.lst.selection_set(0)
            self.show()
        else:
            self.detail.configure(state='normal')
            self.detail.delete('1.0','end')
            self.detail.insert('end','Aucune source ne correspond. Les nouvelles plateformes peuvent être ajoutées au registre versionné.')
            self.detail.configure(state='disabled')

    def show(self):
        selected=self.lst.curselection()
        if not selected:return
        r=self.filtered[selected[0]]
        msg=[r['platform'],'='*max(10,len(r['platform'])),'',
            'ÉTAT : '+r['platform_doc_status'],
            'Connecteur DaAT : NON QUALIFIÉ (catalogue seulement)',
            'Familles : '+', '.join(r['family_labels']),'',
            'VOIES ENVISAGÉES :']
        for a in r['access_paths']:
            msg.append('  - '+a['label']+' ['+a['doc_status']+']')
        msg += ['', 'VOIE PRIVILÉGIÉE : '+r['preferred_path'],
                'CONTENU : '+r['information_scope'],
                'CONDITIONS : '+r['prerequisites'],
                'LIMITES : '+r['blocking_limits'],
                'BOUCLE CHATGPT : '+r['chatgpt_policy'],'',
                'DOCUMENTATION FOURNISSEUR :']
        msg += ['  '+u for u in r['source_reference_urls']] or ['  Non vérifiée à ce stade']
        msg += ['','Une fiche ne constitue ni licence, ni accès effectif, ni autorisation de produire un Kristal.']
        self.detail.configure(state='normal')
        self.detail.delete('1.0','end')
        self.detail.insert('end','\n'.join(msg))
        self.detail.configure(state='disabled')

    def copy(self):
        value=self.detail.get('1.0','end').strip()
        self.top.clipboard_clear()
        self.top.clipboard_append(value)

if __name__=='__main__':
    top=tk.Tk()
    Browser(top)
    top.mainloop()
