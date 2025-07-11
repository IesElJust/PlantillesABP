# PlantillesABP

Plantilles per treballar amb ABP als CFGS de l'IES El Just

Les plantilles i els exemples estan generats amb [mkdocs](https://www.mkdocs.org/) amb la plantilla [Material](https://squidfunk.github.io/mkdocs-material/).

Per tal de treballar amb mkdocs, caldrà generar un entorn virtual Python i activar-lo. Per a això:

1. Creem un nou entorn virtual

```bash
python3 -m venv venv
```

Això ens generarà una carpeta `venv` al directori on ens trobem. Si esteu a l'arrel del projecte, el `.gitignore` farà que aquesta carpeta no es puge a github.

2. Activem l'entorn virtual amb

```bash
. venv/bin/activate
```

3. Dins l'entorn (Veurem que ens diu `(venv)` davant el prompt, instal·lem mkdocs, la plantilla material, i les llibreries Pandas o ODFPy per generar els RAs i CAs a partir dels fulls de càlcul:

```bash
pip install mkdocs mkdocs-material pandas odfpy
```

4. També haurem de registrar el plugin persinalitzat per a la importació de les taules de RAS i CAs als projectes Per a això, dins la carpeta `my_plugin` de cada projecte haurem de fer:

```
pip install -e .
```


5. Amb això ja podreu accedir a la carpeta de la plantilla (`plantillaGeneral`) o a algun exemple (per exemple `Exemples/ProxiMarkt`) i servir el lloc:
 
```
mkdocs serve
```

Generalment, el tindreu disponible en l'adreça: `http://127.0.0.1:8000`.

>
> Addicionalment, si voleu fer ús de la plantilla `plantillaGeneralFull`, caldrà instal·lar `pip install mkdocs-material[imaging]`.
> 


5. Per desactivar l'entorn virtual, només haureu de teclejar l'ordre:

```
deactivate
```

## Extracció dels RAs i CAs dins els projectes


La informació dels RAs i CAs que treballarem en els projectes es troba a un full de càlcul. El plugin personalitzat `replace_ra_ca`, que podem configurar des d'mkdocs ens permet incorporar els RAs i CAs en el projecte sense haver de copiar-los cada vegada. Per exemple, per al projecte ProxiMarkt, fem la següent configuració:

```yaml
plugins:
  - search
  - replace_ra_ca:
      ods_path: "ProjectesDAM.ods"
```

On el paràmetre `ods_path` ens permet indicar quin és el fitxer amb el full de càlcul on tenim els RAs.

Amb aquest plugin, podem especificar, de moment dos marques dins els nostre fitxers mkdocs:

* `{{Full_Projecte&&Modul}}`: Busca el full Full_Projecte dins el fitxer .ods, i incorpora d'aquest projecte tots els RAs i CAs del mòdul especificat, dins una taula. Per exemple, dins el document de seqüenciació de ProxiMarkt trobem `{{ProxiMarkt&&AD}}`, que insereix una taula amb tots els RAs i CAs del projecte per al mòdul *AD*.
* `{{Full_Projecte&&Modul&&Sprint}}`: Busca el full Full_Projecte dins el fitxer .ods, i incorpora una llista e tots els RAs i CAs del mòdul especificat i de l'sprint especificat, en forma de llista. Per exemple, dins el document `docs/sprint_1/AD.md` de ProxiMarkt trobem `{{ProxiMarkt&&AD&&Sprint 1}}`, que insereix una llista amb tots els RAs i CAs de l'Sprint 1 per al mòdul *AD*.

## Format del fitxer de projectes

El fitxer per als projectes (`ProjectesDAM.ods`, `ProjectesDAW.ods` i `ProjectesASIX.ods`) contindran els RAS i CAs utilitzats als diferents projectes. 

Per a cada projecte, crearem un full dins aquest document, amb la plantilla de RAs i CAs d'aquest, ordenats en sprints.

>
> És important no modificar l'ordre ni el nom de les caselles de la capçalera i els mòduls, per preservar el funcionament del plugin que agafa d'aci els continguts.
>

Cada full conté una columna al final de les columnes dels sprints amb tots els RAs/CAs utilitzats al projecte.

Existeix un full Resum amb tots els RAs i CAs utilitzats en els diferents projectes. Cada vegada que incorporem un nou projecte al full, haurem de seguir el mateix esquema que als altres fulls, i a més, haurem d'actualizar aquest full de ressum, incorporant una columna per al nou projecte.

D'aquesta manera, en el full de Resum tindrem tots els RAs i CAs que es tractaran a cada mòdul a través de projectes.

