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
import requests

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
        #dispatcher.utter_message(text=tamanio_room)
    
        arreglo_tamanio = tamanio_room.split("x")
        tamanio_x = arreglo_tamanio[0] 
        tamanio_z = arreglo_tamanio[1]
        #dispatcher.utter_message(text=str(tamanio_x))

        #dispatcher.utter_message(text=str(tamanio_z))

        room_id = tracker.get_slot("numero_id")
        id_a_guardar = room_id
        
        room_id = int(room_id) + 1
        #id con el formato room-1 para que se pueda encontrar en el mundo sintético y para que se puede obtener el id para photon
        room_id = "room-" + str(room_id)
        myobj = {
                "agilebotId": "Gianluca",
                "method": "CrearRoom",
                "parameters": {"room_id": room_id, "tamanio_x": tamanio_x, tamanio_z: "tamanio_z"}
                }
        #determinar que hacer con la respuesta para mandarle los datos a unity o responder que no se puede crear el room
        x = requests.post(url, data = myobj)    

        #solo incrementar el id si se pudo crear el room
        id_a_guardar = id_a_guardar + 1.0
        return [SlotSet("numero_id", id_a_guardar)]  
        
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
            #probablemente deba hacer una acción que resetee los slots y pregunte de nuevo o vuelva a preguntar las posiciones
            #Seguro sea mejor lo segundo
            dispatcher.utter_message(text="Al parecer ingresó una cantidad diferente de posiciones a la cantidad de objetos especificada")
            return [SlotSet("posicion", None)]   

        for pos in arreglo_posicion:    
            
            pos = str(pos)
            pos_x = pos.split(",")[0]
            pos_z = pos.split(",")[1]

            object_id = tracker.get_slot("numero_id")
            id_a_guardar = object_id
        
            object_id = int(object_id) + 1
            #id con el formato room-1 para que se pueda encontrar en el mundo sintético y para que se puede obtener el id para photon
            object_id = "room-" + str(object_id)
            myobj = {
                "agilebotId": "Gianluca",
                "method": "CrearObjeto",
                "parameters": {"room_id": "room-1", 
                                "parameters": {"object_id": object_id, "prefab": objeto, "pos_x": pos_x, "pos_z": pos_z }
                }
            }
            #determinar que hacer con la respuesta para mandarle los datos a unity o responder que no se puede crear el room
            x = requests.post(url, data = myobj)    

            #solo incrementar el id si se pudo crear el objeto (segun la respuesta)
            id_a_guardar = id_a_guardar + 1.0

        return [SlotSet("numero_id", id_a_guardar)]  
     
