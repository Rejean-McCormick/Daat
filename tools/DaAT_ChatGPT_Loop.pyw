# -*- coding: utf-8 -*-
"""DaAT manual ChatGPT loop: Windows GUI, no terminal or network integration."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
from daat.chatgpt_loop import make_bundle, validate_chatgpt_response, verify_bundle, make_repair_prompt
from daat.errors import DaatError
from daat.output import write_private_json


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('DaAT — Boucle ChatGPT (propositions non canoniques)')
        self.minsize(780, 720)
        self.geometry('1040x810')
        self.sources: list[dict] = []
        self.bundle = None
        self.draft = None
        self.last_error_code = None
        self._make_ui()

    def _make_ui(self):
        base = ttk.Frame(self, padding=12)
        base.pack(fill='both', expand=True)
        ttk.Label(base, text='DaAT × ChatGPT · Lecture autorisée → prompt → réponse → brouillon',
                  font=('Segoe UI', 14, 'bold')).pack(anchor='w')
        ttk.Label(base, text='Aucune connexion Medium, PhilPapers ou ChatGPT automatique. '
                  'Ne collez jamais de mot de passe ni de cookie. Les résultats ne sont pas des Kristals canoniques.',
                  foreground='#7a4a00', wraplength=960).pack(anchor='w', pady=(4, 10))
        self.tabs = ttk.Notebook(base)
        self.tabs.pack(fill='both', expand=True)
        self.source_tab = ttk.Frame(self.tabs, padding=10)
        self.prompt_tab = ttk.Frame(self.tabs, padding=10)
        self.response_tab = ttk.Frame(self.tabs, padding=10)
        self.tabs.add(self.source_tab, text='1 · Sources')
        self.tabs.add(self.prompt_tab, text='2 · Prompt')
        self.tabs.add(self.response_tab, text='3 · Réponse et vérification')
        self._source_ui()
        self._prompt_ui()
        self._response_ui()
        self.status = tk.StringVar(value='Prêt · Texte local uniquement, zéro scraping')
        ttk.Label(base, textvariable=self.status, wraplength=970).pack(anchor='w', pady=(8, 0))

    def _form_row(self, parent, label, variable, row, *, choices=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=3)
        if choices:
            widget = ttk.Combobox(parent, textvariable=variable, values=choices, state='readonly')
        else:
            widget = ttk.Entry(parent, textvariable=variable)
        widget.grid(row=row, column=1, sticky='ew', padx=(8, 0), pady=3)
        return widget

    def _source_ui(self):
        pane = self.source_tab
        frm = ttk.Frame(pane)
        frm.pack(fill='x')
        frm.columnconfigure(1, weight=1)
        self.provider = tk.StringVar(value='Medium')
        self.title_var = tk.StringVar()
        self.url = tk.StringVar()
        self.scope = tk.StringVar(value='summary')
        self.access = tk.StringVar(value='user_paste')
        self.rights_basis = tk.StringVar(value='Contenu communiqué par l’utilisateur pour analyse autorisée')
        self.purpose = tk.StringVar(value='Préparer des composants possibles de Kristal, pour revue humaine')
        self._form_row(frm, 'Plateforme / source', self.provider, 0)
        self._form_row(frm, 'Titre', self.title_var, 1)
        self._form_row(frm, 'Lien public facultatif (sans identifiants)', self.url, 2)
        self._form_row(frm, 'Contenu effectivement accessible', self.scope, 3,
                       choices=['metadata', 'summary', 'excerpt', 'full_text'])
        self._form_row(frm, 'Mode d’acquisition', self.access, 4,
                       choices=['user_paste', 'manual_browser_copy', 'authorized_export'])
        self._form_row(frm, 'Base de droits / conditions', self.rights_basis, 5)
        self._form_row(frm, 'Objectif', self.purpose, 6)
        ttk.Label(pane, text='Texte de la source (coller un résumé, extrait, export ou article autorisé) :').pack(anchor='w', pady=(10, 2))
        self.source_text = tk.Text(pane, height=12, wrap='word', undo=True)
        self.source_text.pack(fill='both', expand=True)
        buttons = ttk.Frame(pane)
        buttons.pack(fill='x', pady=(5, 8))
        ttk.Button(buttons, text='Charger .txt/.md autorisé', command=self.load_text).pack(side='left')
        ttk.Button(buttons, text='Ajouter source', command=self.add_source).pack(side='left', padx=8)
        ttk.Button(buttons, text='Retirer source sélectionnée', command=self.remove_source).pack(side='left')
        self.source_list = tk.Listbox(pane, height=4)
        self.source_list.pack(fill='x')
        self.ack_rights = tk.BooleanVar(value=False)
        self.ack_share = tk.BooleanVar(value=False)
        ttk.Checkbutton(pane, variable=self.ack_rights,
                        text='Je confirme que je peux utiliser ce contenu aux fins déclarées.').pack(anchor='w', pady=(7, 0))
        ttk.Checkbutton(pane, variable=self.ack_share,
                        text='Je confirme pouvoir transmettre ce texte à ChatGPT (service tiers), selon les droits applicables.').pack(anchor='w')
        ttk.Button(pane, text='Créer le prompt →', command=self.build).pack(anchor='e', pady=8)

    def _prompt_ui(self):
        p = self.prompt_tab
        ttk.Label(p, text='Copie manuelle dans ChatGPT. Vérifie le texte avant de le divulguer.',
                  wraplength=900).pack(anchor='w', pady=(0, 6))
        self.prompt_text = tk.Text(p, wrap='word', undo=False)
        self.prompt_text.pack(fill='both', expand=True)
        row = ttk.Frame(p)
        row.pack(anchor='e', pady=8)
        ttk.Button(row, text='Copier le prompt', command=self.copy_prompt).pack(side='left', padx=5)
        ttk.Button(row, text='Enregistrer le paquet privé', command=self.save_bundle).pack(side='left', padx=5)
        ttk.Button(row, text='Charger un paquet privé', command=self.load_bundle).pack(side='left', padx=5)
        ttk.Button(row, text='Réponse ChatGPT →', command=lambda: self.tabs.select(self.response_tab)).pack(side='left', padx=5)

    def _response_ui(self):
        p = self.response_tab
        ttk.Label(p, text='Colle ici le JSON brut retourné par ChatGPT. Vérification structurelle et citations exactes seulement.',
                  wraplength=930).pack(anchor='w', pady=(0, 6))
        self.response_text = tk.Text(p, wrap='word', undo=True)
        self.response_text.pack(fill='both', expand=True)
        controls = ttk.Frame(p)
        controls.pack(fill='x', pady=8)
        ttk.Button(controls, text='Coller depuis le presse-papiers', command=self.paste_response).pack(side='left', padx=4)
        ttk.Button(controls, text='Vérifier le JSON', command=self.verify_response).pack(side='left', padx=4)
        ttk.Button(controls, text='Exporter le brouillon privé', command=self.save_draft).pack(side='left', padx=4)
        ttk.Button(controls, text='Prompt de correction', command=self.repair_prompt).pack(side='left', padx=4)
        self.result_text = tk.Text(p, height=11, wrap='word', state='disabled')
        self.result_text.pack(fill='x')

    def _error(self, title, exc):
        messagebox.showerror(title, str(exc))
        self.status.set(f'{title} : {exc}')

    def load_text(self):
        path = filedialog.askopenfilename(title='Texte local autorisé', filetypes=[('Textes', '*.txt *.md'), ('Tous fichiers', '*.*')])
        if not path:
            return
        try:
            p = Path(path)
            if not p.is_file() or p.is_symlink() or p.stat().st_size > 160_000:
                raise ValueError('Fichier absent, lié ou trop volumineux (160 Ko maximum).')
            data = p.read_text(encoding='utf-8-sig')
            if len(data) > 40_000:
                raise ValueError('Texte trop long (40 000 caractères par source).')
            self.source_text.delete('1.0', 'end')
            self.source_text.insert('1.0', data)
            self.status.set('Texte local chargé. Aucun envoi externe effectué.')
        except Exception as exc:
            self._error('Lecture refusée', exc)

    def add_source(self):
        try:
            item = {'provider': self.provider.get(), 'title': self.title_var.get(),
                    'locator': self.url.get(), 'scope': self.scope.get(),
                    'access_method': self.access.get(), 'rights_basis': self.rights_basis.get(),
                    'text': self.source_text.get('1.0', 'end-1c')}
            # Validate immediately without retaining a model prompt or consenting by proxy.
            make_bundle([item], purpose=self.purpose.get(), user_rights_confirmed=True,
                        chatgpt_disclosure_confirmed=True)
            if len(self.sources) >= 6:
                raise ValueError('Maximum 6 sources par session.')
            self.sources.append(item)
            self.source_list.insert('end', f'{len(self.sources)} · {item["provider"]} · {item["scope"]} · {item["title"]}')
            self.source_text.delete('1.0', 'end')
            self.title_var.set('')
            self.url.set('')
            self.bundle = None
            self.draft = None
            self.status.set(f'{len(self.sources)} source(s) ajoutée(s) en mémoire locale.')
        except Exception as exc:
            self._error('Source invalide', exc)

    def remove_source(self):
        sel = self.source_list.curselection()
        if not sel:
            return
        self.sources.pop(sel[0])
        self.source_list.delete(0, 'end')
        for i, item in enumerate(self.sources, 1):
            self.source_list.insert('end', f'{i} · {item["provider"]} · {item["scope"]} · {item["title"]}')
        self.bundle = None
        self.draft = None
        self.status.set('Liste modifiée : régénère le prompt avant de traiter une réponse.')

    def build(self):
        try:
            self.bundle = make_bundle(self.sources, purpose=self.purpose.get(),
                user_rights_confirmed=self.ack_rights.get(),
                chatgpt_disclosure_confirmed=self.ack_share.get())
            self.draft = None
            self.prompt_text.delete('1.0', 'end')
            self.prompt_text.insert('1.0', self.bundle['prompt'])
            self.tabs.select(self.prompt_tab)
            self.status.set(f'Prompt créé · {len(self.sources)} source(s) · Non envoyé. Citation exacte exigée.')
        except Exception as exc:
            self._error('Prompt refusé', exc)

    def copy_prompt(self):
        if self.bundle is None:
            self._error('Aucun prompt', 'Ajoute des sources et crée le prompt.')
            return
        self.clipboard_clear()
        self.clipboard_append(self.prompt_text.get('1.0', 'end-1c'))
        self.update()
        self.status.set('Prompt copié dans le presse-papiers. À coller manuellement dans ChatGPT.')

    def paste_response(self):
        try:
            data = self.clipboard_get()
            if len(data) > 250_000:
                raise ValueError('Réponse trop longue.')
            self.response_text.delete('1.0', 'end')
            self.response_text.insert('1.0', data)
        except Exception as exc:
            self._error('Collage refusé', exc)

    def verify_response(self):
        try:
            if self.bundle is None:
                raise ValueError('Crée ou charge le paquet du prompt correspondant avant la vérification.')
            text = self.response_text.get('1.0', 'end-1c')
            if len(text) > 250_000:
                raise ValueError('Réponse trop longue.')
            answer = json.loads(text, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Constante JSON invalide')))
            self.draft = validate_chatgpt_response(self.bundle, answer)
            self.last_error_code = None
            candidates = self.draft['candidate_parts']
            brief = (f'Vérification locale réussie : {len(candidates)} proposition(s) à revoir.\n'
                     f'{len(self.draft["unknowns"])} incertitude(s). Aucune autorisation de construire ou publier.\n\n')
            for row in candidates:
                sources = ', '.join(x['source_id'] for x in row['evidence'])
                limited = any(x['limited_to_supplied_material'] for x in row['evidence'])
                brief += f'- {row["kind"]} ({"matériau partiel" if limited else "texte déclaré complet"}) : {row["text"][:150]} [{sources}]\n'
            self.result_text.configure(state='normal')
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('1.0', brief)
            self.result_text.configure(state='disabled')
            self.status.set('Citations exactes vérifiées; vérité, droits et admissibilité Kit NON vérifiés.')
        except Exception as exc:
            self.draft = None
            self.last_error_code = getattr(exc, 'code', None)
            self._error('Réponse refusée', exc)

    def repair_prompt(self):
        try:
            if self.bundle is None or self.last_error_code is None:
                raise ValueError('Aucun rejet réparable. Vérifie d’abord une réponse JSON.')
            repaired = make_repair_prompt(self.bundle, self.last_error_code)
            self.prompt_text.delete('1.0', 'end')
            self.prompt_text.insert('1.0', repaired)
            self.tabs.select(self.prompt_tab)
            self.status.set('Prompt de correction prêt à copier manuellement. Réponse précédente non acceptée.')
        except Exception as exc:
            self._error('Correction impossible', exc)

    def _save(self, obj, label, filename):
        if obj is None:
            messagebox.showinfo('Aucun résultat', f'{label} inexistant.')
            return
        path = filedialog.asksaveasfilename(title=label, initialfile=filename, defaultextension='.json',
                                            filetypes=[('JSON privé', '*.json')])
        if not path:
            return
        try:
            write_private_json(Path(path), obj)
            self.status.set(f'{label} enregistré localement : {Path(path).name}. Attention : contient des citations et sources.')
        except Exception as exc:
            self._error('Écriture refusée', exc)

    def save_bundle(self):
        self._save(self.bundle, 'Paquet du prompt', 'daat-chatgpt-prompt-prive.json')

    def save_draft(self):
        self._save(self.draft, 'Brouillon de propositions', 'daat-propositions-non-canoniques.json')

    def load_bundle(self):
        path = filedialog.askopenfilename(title='Paquet de prompt précédent', filetypes=[('JSON', '*.json')])
        if not path:
            return
        try:
            p = Path(path)
            if p.is_symlink() or p.stat().st_size > 800_000:
                raise ValueError('Fichier lié ou trop grand')
            bundle = json.loads(p.read_text(encoding='utf-8'))
            verify_bundle(bundle)
            self.bundle = bundle
            self.draft = None
            self.prompt_text.delete('1.0', 'end')
            self.prompt_text.insert('1.0', bundle['prompt'])
            self.tabs.select(self.prompt_tab)
            self.status.set('Paquet précédent chargé et empreintes vérifiées. Aucune nouvelle autorisation déduite.')
        except Exception as exc:
            self._error('Paquet refusé', exc)


if __name__ == '__main__':
    Window().mainloop()
