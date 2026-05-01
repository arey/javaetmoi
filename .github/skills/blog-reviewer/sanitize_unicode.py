#!/usr/bin/env python3
"""
sanitize_unicode.py — Remplace les caractères typographiques Unicode générés
par les LLM par leurs équivalents ASCII dans un fichier Markdown Hugo.

Les blocs de code (``` ... ```) et les URLs sont préservés intacts.

Usage :
    python sanitize_unicode.py <fichier.md>
    python sanitize_unicode.py <fichier.md> --dry-run
"""

import re
import sys
import argparse
from pathlib import Path

# Table de substitution : (unicode, remplacement ASCII, description)
SUBSTITUTIONS = [
    ("\u2026", "...",  "points de suspension"),
    ("\u2013", "-",    "tiret demi-cadratin (en dash)"),
    ("\u2014", "--",   "tiret cadratin (em dash)"),
    ("\u2012", "-",    "tiret figuratif"),
    ("\u2018", "'",    "guillemet simple ouvrant"),
    ("\u2019", "'",    "guillemet simple fermant / apostrophe"),
    ("\u201c", '"',    "guillemet double ouvrant"),
    ("\u201d", '"',    "guillemet double fermant"),
    ("\u201e", '"',    "guillemet double bas"),
    ("\u00ab", "<<",   "guillemet français ouvrant"),
    ("\u00bb", ">>",   "guillemet français fermant"),
    ("\u00a0", " ",    "espace insécable"),
    ("\u2009", " ",    "espace fine"),
    ("\u202f", " ",    "espace fine insécable"),
    ("\u00d7", "x",    "signe multiplication"),
    ("\u2713", "ok",   "coche (check mark)"),
    ("\u2717", "x",    "croix"),
    ("\u2022", "-",    "puce (bullet)"),
    ("\u2032", "'",    "prime (minutes/pieds)"),
    ("\u2033", '"',    "double prime (secondes/pouces)"),
]

# Regex pour isoler les zones à NE PAS toucher :
#   - blocs de code fencés  (``` ... ```)
#   - URLs (http:// ou https:// jusqu'à la fin du token)
_PROTECTED = re.compile(
    r"(```[\s\S]*?```"       # bloc de code fencé (non-greedy)
    r"|`[^`\n]*`"            # code inline
    r"|https?://\S+"         # URL
    r")",
    re.MULTILINE,
)


def _apply_substitutions(text: str) -> tuple[str, dict[str, int]]:
    """Applique les substitutions hors zones protégées.

    Retourne (texte_modifié, compteurs_par_caractère).
    """
    counters: dict[str, int] = {}

    # Découper le texte en segments : protégés (impairs) / libres (pairs)
    parts = _PROTECTED.split(text)
    result_parts = []

    for i, part in enumerate(parts):
        if i % 2 == 1:
            # Zone protégée — conserver tel quel
            result_parts.append(part)
        else:
            # Zone libre — appliquer les substitutions
            for char, replacement, name in SUBSTITUTIONS:
                count = part.count(char)
                if count:
                    part = part.replace(char, replacement)
                    counters[name] = counters.get(name, 0) + count
            result_parts.append(part)

    return "".join(result_parts), counters


def sanitize_file(path: Path, dry_run: bool = False) -> bool:
    """Lit, nettoie et réécrit le fichier.

    Retourne True si des modifications ont été effectuées.
    """
    original = path.read_text(encoding="utf-8")
    cleaned, counters = _apply_substitutions(original)

    if not counters:
        print(f"[OK] Aucun caractère à remplacer dans {path}")
        return False

    print(f"[{'DRY-RUN' if dry_run else 'FIXED'}] {path}")
    for name, count in sorted(counters.items(), key=lambda x: -x[1]):
        print(f"  {count:3d}x  {name}")

    if not dry_run:
        path.write_text(cleaned, encoding="utf-8")
        print(f"  => {path} mis à jour.")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remplace les caractères Unicode LLM par leurs équivalents ASCII."
    )
    parser.add_argument("files", nargs="+", metavar="fichier.md",
                        help="Fichier(s) Markdown à traiter")
    parser.add_argument("--dry-run", action="store_true",
                        help="Afficher les substitutions sans modifier les fichiers")
    args = parser.parse_args()

    changed = 0
    for file_arg in args.files:
        path = Path(file_arg)
        if not path.exists():
            print(f"[ERREUR] Fichier introuvable : {path}", file=sys.stderr)
            sys.exit(1)
        if sanitize_file(path, dry_run=args.dry_run):
            changed += 1

    print(f"\n{changed}/{len(args.files)} fichier(s) modifié(s).")


if __name__ == "__main__":
    main()
