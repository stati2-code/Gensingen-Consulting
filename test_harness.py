
# -*- coding: utf-8 -*-
from noah_g_agent_core import route_task
import sys

# HINWEIS: Dies stellt sicher, dass das Terminal UTF-8 für die Ausgabe verwendet.
sys.stdout.reconfigure(encoding='utf-8')

print("Starte ausgiebigen Funktions- und Usability-Test...")
print("="*50)

test_prompts = [
    # Eindeutige Fälle
    "Baue eine neue Microsite.",
    "Ich möchte den Footer auf der Startseite ändern.",
    "Führe bitte die monatliche SEO Wartung durch.",
    "Kannst du das Menü überarbeiten?",

    # Grenzfälle
    "Wie ist der Status?", # Sollte Fallback auslösen
    "Optimiere die Ladezeit und ändere das Logo.", # Gemischte Absicht

    # Umlaut-Test
    "Ändere den Text auf der 'Über Uns' Seite."
]

for i, prompt in enumerate(test_prompts):
    print(f"\n--- Testfall {i+1} ---")
    print(f"Eingabe: '{prompt}'")
    result = route_task(prompt)
    print(f"Ausgabe: {result}")
    print("-"*20)

print("="*50)
print("Testlauf abgeschlossen.")
