
# -*- coding: utf-8 -*-
"""
**Kernlogik des Sub-Agenten "NOAH G"**

Dieses Skript ist das zentrale Nervensystem des Agenten. Es beinhaltet die Routing-Logik,
um eingehende Aufgaben dem korrekten strategischen Arbeitsmodell zuzuordnen.
"""

# Hypothetische Importe der Modus-Implementierungen
# from modes import architect, renovator, gardener
# from tools import wordpress_api

def route_task(prompt: str):
    """Analysiert den Prompt und leitet ihn an das passende Arbeitsmodell weiter."""
    
    # --- Normalisierung der Umlaute für Robustheit ---
    prompt_lower = prompt.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    
    # --- Schlüsselwörter für die Modus-Erkennung (jetzt ohne Umlaute) ---
    architect_keywords = ['neu', 'relaunch', 'von grund auf', 'bau', 'erstelle', 'scaffolding', 'neues projekt']
    renovator_keywords = ['aendere', 'repariere', 'aktualisiere', 'passe an', 'fix', 'update', 'modiiziere', 'ueberarbeite']
    gardener_keywords = ['wartung', 'seo', 'performance', 'blogbeitrag', 'pflege', 'check', 'optimier', 'regelmaessig']
    
    # --- Zählung der Absichten ---
    detected_modes = []
    if any(keyword in prompt_lower for keyword in architect_keywords):
        detected_modes.append("architect")
    if any(keyword in prompt_lower for keyword in renovator_keywords):
        detected_modes.append("renovator")
    if any(keyword in prompt_lower for keyword in gardener_keywords):
        detected_modes.append("gardener")

    # --- Verbesserte Routing-Logik ---
    if len(detected_modes) > 1:
        print(f"WARNUNG: Mehrere Absichten erkannt: {detected_modes}. Bitte formulieren Sie separate Anweisungen.")
        return {"mode": "clarification_needed", "status": "Mehrere Absichten"}
    elif len(detected_modes) == 1:
        mode = detected_modes[0]
        print(f"INFO: {mode.capitalize()}-Modus wird aktiviert.")
        return {"mode": mode, "status": "Routing erfolgreich"}
    else:
        print("WARNUNG: Kein spezifischer Modus erkannt. Standard-Modus (Renovierer) wird als Fallback genutzt.")
        return {"mode": "renovator", "status": "Fallback-Routing"}

# --- Beispiel-Aufrufe zur Demonstration ---

if __name__ == '__main__':
    task1 = "Erstelle eine komplett neue Webseite für einen Kunden."
    task2 = "Ich muss den Footer auf der Startseite ändern."
    task3 = "Führe einen monatlichen SEO-Check durch."
    task4 = "Wie spät ist es?"
    
    print(f"Task: '{task1}' -> Geroutet zu: {route_task(task1)}")
    print(f"Task: '{task2}' -> Geroutet zu: {route_task(task2)}")
    print(f"Task: '{task3}' -> Geroutet zu: {route_task(task3)}")
    print(f"Task: '{task4}' -> Geroutet zu: {route_task(task4)}")

