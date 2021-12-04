# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions.event_handling import EventPublisher

import json

url='http://127.0.0.1:5000/dispatcher/send-message'  
    
class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")

         return []

class ActionGuardarNombre(Action):
    def name(self) -> Text:
        return "action_guardar_nombre"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nombre = next(tracker.get_latest_entity_values("nombre"), None)
        text = str(nombre)
        
        message=f"Un placer conocerle {text}, en que puedo auyudarle?"
        dispatcher.utter_message(text=str(message))
        
        return [SlotSet("nombre",text)]      

class ActionGuardarTamanio(Action):
    def name(self) -> Text:
        return "action_guardar_tamanio"  

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tamanio_room = str(tracker.get_slot("tamanio_room"))
            
        arreglo_tamanio = tamanio_room.split("x")
        tamanio_x = arreglo_tamanio[0] 
        tamanio_z = arreglo_tamanio[1]
        
        dispatcher.utter_message(text = "Crear room," + tamanio_x + "," + tamanio_z)
        return [SlotSet("tamanio_x", tamanio_x), SlotSet("tamanio_z", tamanio_z)]  
        
class ActionGuardarObjeto(Action):

    def name(self) -> Text:
        return "action_guardar_objeto"  

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        objeto = str(tracker.get_slot("objeto"))
        cantidad = tracker.get_slot("cantidad")
       
        posicion = str(tracker.get_slot("posicion"))
        posicion = posicion.replace(" ", "")
        
        arreglo_posicion = posicion.split(";")
        
        if(len(arreglo_posicion) != int(cantidad)):
            dispatcher.utter_message(text="Al parecer ingresó una cantidad diferente de posiciones a la cantidad de objetos especificada")
            return [SlotSet("posicion", None)]   

        for pos in arreglo_posicion:    
            
            pos = str(pos)
            pos_x = pos.split(",")[0]
            pos_z = pos.split(",")[1]
            dispatcher.utter_message(text = "Crear objeto," + objeto + "," + pos_x + "," + pos_z)
        
        return []  
     
