
# -*- coding: utf-8 -*-
"""
**Toolset-Architektur für den Sub-Agenten "Der digitale Architekt"**

Dieses Modul definiert die High-Level-Schnittstelle für die Interaktion
mit einer WordPress-Instanz. Es abstrahiert die Komplexität von XML-RPC-Aufrufen
in saubere, aufgabenorientierte Python-Funktionen.
"""

import dataclasses
import subprocess
import xml.etree.ElementTree as ET
from typing import Literal, List, Dict, Any, Optional

# --- Dataclasses für klare Strukturen ---

@dataclasses.dataclass
class Post:
    id: int
    title: str
    content: str
    status: str
    post_type: str
    slug: str

# --- Haupt-API-Klasse ---

class WordPressClient:
    """Der primäre Client für die Interaktion mit WordPress."""

    def __init__(self, xmlrpc_url: str, username: str, password: str):
        self.xmlrpc_url = xmlrpc_url
        self.username = username
        self.password = password

    def _build_xml_payload(self, method_name: str, params: tuple) -> bytes:
        """Baut die XML-Payload für einen XML-RPC-Aufruf."""
        method_call = ET.Element("methodCall")
        ET.SubElement(method_call, "methodName").text = method_name
        params_element = ET.SubElement(method_call, "params")
        
        for param_data in params:
            param = ET.SubElement(params_element, "param")
            value = ET.SubElement(param, "value")
            if isinstance(param_data, int):
                ET.SubElement(value, "int").text = str(param_data)
            elif isinstance(param_data, str):
                ET.SubElement(value, "string").text = str(param_data)
            elif isinstance(param_data, dict):
                struct = ET.SubElement(value, "struct")
                for key, val in param_data.items():
                    member = ET.SubElement(struct, "member")
                    ET.SubElement(member, "name").text = key
                    member_value = ET.SubElement(member, "value")
                    # Annahme: Alle Werte im Struct sind Strings
                    ET.SubElement(member_value, "string").text = str(val)

        return ET.tostring(method_call, encoding='utf-8', method='xml')

    def _execute_xmlrpc(self, method_name: str, params: tuple) -> str:
        """Führt einen XML-RPC-Aufruf sicher über curl.exe aus."""
        xml_payload = self._build_xml_payload(method_name, params)

        command = [
            "curl.exe",
            "-X", "POST",
            "-d", xml_payload,
            self.xmlrpc_url
        ]

        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                check=True
            )
            if "<fault>" in result.stdout:
                raise ValueError(f"XML-RPC Error: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_message = f"XML-RPC call failed: {e.stderr}"
            print(error_message)
            raise
        except FileNotFoundError:
            print("Error: curl.exe not found. Please ensure it is in your system's PATH.")
            raise

    def get_content(self, post_id: int) -> str:
        """Ruft den Inhalt eines spezifischen Beitrags oder einer Seite ab."""
        blog_id = 252499783 
        params = (blog_id, post_id, self.username, self.password)
        return self._execute_xmlrpc("wp.getPage", params)

    def update_content(self, post_id: int, content: str, title: Optional[str] = None) -> bool:
        """
        Aktualisiert den Inhalt und optional den Titel einer Seite.
        """
        blog_id = 252499783
        
        content_struct = {
            'post_content': content,
            'post_status': 'publish' # Wichtig, damit die Seite nicht als Entwurf gespeichert wird
        }
        if title:
            content_struct['post_title'] = title
            
        params = (blog_id, post_id, self.username, self.password, content_struct)
        
        try:
            response = self._execute_xmlrpc("wp.editPage", params)
            # wp.editPage gibt bei Erfolg `True` zurück.
            # Wir prüfen, ob die Antwort eine Erfolgsmeldung enthält.
            return "<boolean>1</boolean>" in response
        except ValueError as e:
            print(f"Failed to update content for post {post_id}: {e}")
            return False
