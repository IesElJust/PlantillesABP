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

>
> És possible que tambè hàgeu de registrar el plugin persinalitzat per a la importació de les taules de RAS i CAs als projectes Per a això, en l'arrel de cada projecte (comproveu que hi ha una carpeta my_plugin):
>
> ```
> pip install -e .
> ```


4. Amb això ja podreu accedir a la carpeta de la plantilla (`plantillaGeneral`) o a algun exemple (per exemple `Exemples/ProxiMarkt`) i servir el lloc:
 
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