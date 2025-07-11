import re
import os
import pandas as pd
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class ReplaceRaCaPlugin(BasePlugin):
    config_scheme = [
        ('ods_path', config_options.Type(str))  # Utilitza config_options.Type(str)
    ]
        
    def on_config(self, config):
        # Carrega només una vegada l'ODS
        #ods_path = config.get('replace_ra_ca', {}).get('ods_path', 'Projectes.ods')
        #print('INFO    -  [replace_ra_ca] plugin. Setting ods_path to '+ods_path)

        #self.ods_path = os.path.join(os.path.dirname(config.config_file_path), ods_path)

        # Llegim el fitxer ODS especificat en mkdocs.yml
        ods_path = self.config.get('ods_path', 'Projectes.ods')  # Obtenc el valor de la configuració de plugin
        self.ods_path = os.path.join(os.path.dirname(config.config_file_path), ods_path)
   
        # Carreguem el fitxer ODS
        self.sheets = pd.read_excel(self.ods_path, engine="odf", sheet_name=None)
        
        print(f'INFO    -  [replace_ra_ca] plugin. Setting ods_path to {self.ods_path}')

        return config

    def on_page_markdown(self, markdown, **kwargs):
        # Primer tipus d'etiqueta: {{full&&modul&&sprint}}
        pattern_sprint = r"\{\{([\w_]+)&&(\w+)&&([\w\s]+)\}\}"
        matches = re.findall(pattern_sprint, markdown)

        for full, modul, sprint in matches:
            reemplaç = self.generar_llista(full, modul, sprint)
            etiqueta = f"{{{{{full}&&{modul}&&{sprint}}}}}"
            markdown = markdown.replace(etiqueta, reemplaç)

        # Segon tipus d'etiqueta: {{full&&modul}}
        pattern_modul = r"\{\{([\w_]+)&&(\w+)\}\}"
        matches = re.findall(pattern_modul, markdown)

        # Filtra les que ja hem processat
        matches = [m for m in matches if len(m) == 2]

        for full, modul in matches:
            reemplaç = self.generar_taula(full, modul)
            etiqueta = f"{{{{{full}&&{modul}}}}}"
            markdown = markdown.replace(etiqueta, reemplaç)

        return markdown

    def generar_llista(self, full, modul, sprint):
        try:
            df = self.sheets[full]
        except KeyError:
            return f"⚠️ Full '{full}' no trobat."

        df.columns = df.iloc[0]
        df = df.drop([0, 1]).reset_index(drop=True)

        # Neteja noms de columna
        df.columns = [str(col).strip().replace("\n", " ").replace("\u2003", "").replace("\xa0", "").replace(" ", "") for col in df.columns]

        # Propaga mòduls
        df["Mòduls"] = df["Mòduls"].ffill()
        df = df.fillna("")

        output = []
        ra_prefix = None

        for _, row in df.iterrows():
            modul_actual = str(row["Mòduls"]).strip()
            text = str(row["Resultats d'aprenentatge i Criteris d'Avaluació"]).strip()
            treballat = str(row.get(sprint, "")).strip().lower() == "x"

            if modul_actual == modul and treballat:
                if text.startswith("RA"):
                    # Extreiem el prefix (ex: "RA2")
                    ra_prefix = text.split("-")[0].strip()
                    output.append(f"- **{ra_prefix}-** {text.split('-', 1)[1].strip()}")
                elif ra_prefix:
                    # Prefixem cada criteri amb RAx.letra)
                    match = re.match(r"([a-z]\))\s*(.*)", text, re.IGNORECASE)
                    if match:
                        etiqueta = match.group(1)
                        descripcio = match.group(2)
                        output.append(f"    - **{ra_prefix}.{etiqueta}** {descripcio}")
                    else:
                        output.append(f"    - {text}")  # Per si no segueix el patró habitual

        return "\n".join(output) if output else "_No hi ha criteris marcats per aquest sprint._"

    def generar_taula(self, full, modul):
        try:
            df = self.sheets[full]
        except KeyError:
            return f"⚠️ Full '{full}' no trobat."

        df.columns = df.iloc[0]
        df = df.drop([0, 1]).reset_index(drop=True)
        
    
        df["Mòduls"] = df["Mòduls"].ffill() # 🧠 Aquí propaguem el mòdul

        df = df.fillna("")


        sprint_cols = [col for col in df.columns if str(col).startswith("Sprint")]

        taula = ["| Resultat / Criteri | Treballat? |", "|---|---|"]
        current_ra = ""

        checked_icon="<li class='task-list-item'><input type='checkbox' style='display: none' disabled='' checked=''><span class='task-list-indicator'></span></li>"
        unchecked_icon="<li class='task-list-item'><input type='checkbox' style='display: none'><span class='task-list-indicator'></span></li>"

        for _, row in df.iterrows():
            if row["Mòduls"] == modul:
                text = str(row["Resultats d'aprenentatge i Criteris d'Avaluació"]).strip()
                current_ra = text
                treballat = any(str(row.get(col, "")).lower() == "x" for col in sprint_cols)
                if treballat:
                    taula.append(f"| **{current_ra}** | {checked_icon}  |")
                else:
                    taula.append(f"| {current_ra} | {unchecked_icon}  |")
                #taula.append(f"| **{current_ra}** | {checked_icon if treballat else unchecked_icon} |")
            elif row["Mòduls"] == "" and current_ra:
                treballat = any(str(row.get(col, "")).lower() == "x" for col in sprint_cols)
                taula.append(f"| {text} | {'x' if treballat else ''} |")

        return "\n".join(taula) if len(taula) > 2 else "_Cap resultat o criteri trobat._"
