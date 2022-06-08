from typing import Any, Text, Dict, List
import time
from jinja2 import TemplateAssertionError

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

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

# Desformatea el tamaño de un room y envía el mensaje para que sea utilizado en Unity
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
    """ 
        Obtiene el objeto a crear y la cantidad de los slots. Luego, desformatea las posiciones, 
        verificando que la cantidad obtenida sea igual al número de objetos a crear. Por último, obtiene las posiciones específicas
        y emite un mensaje." 
    """
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
     
class ActionDeterminarRoom(Action):
        def name(self) -> Text: 
            return "action_determinar_room"  

        def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            tema_microlearning = str(tracker.get_slot("tema_microlearning"))
            
            if(tema_microlearning == "crear un room"):
                dispatcher.utter_message(text = "Crear room," + "20"+ "," + "20")
                return[]
                

            #ejemplo de diccionario para cuando haya más rooms, podría ser una lista asi es mutable y que esté predefinida
            romsportema = {
                ("sacar plata del cajero", "sacar plata de un cajero", "saca plata de un cajero", "cambiar la contraseña", "iniciar sesion en mi cuenta del banco", "iniciar sesion en mi cuenta bancaria", "sacar dinero del cajero", "sacar dinero de un cajero") : "RoomBanco"
            }

            #debería poder actualizar roomsportema si se detecta una entidad de tema_microlearning que no esté en el dict

            for key in romsportema.keys():
                if tema_microlearning in key:
                    room_microlearning = romsportema.get(key)

            if(room_microlearning == "RoomBanco"):
                dispatcher.utter_message(text = "Acompañame a un cajero que este libre, por favor")

            dispatcher.utter_message(text = "Room microlearning," + room_microlearning + "," + tema_microlearning)
            
            return[SlotSet("room_microlearning", "RoomBanco")]

        
class ActionResponderDuda(Action):
    def name(self) -> Text:
        return "action_responder_duda"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        DUDA_LONG = "longitud contraseña"

        duda = next(tracker.get_latest_entity_values("duda"), None)
        duda = str(duda)

        respuestasdudatuple = {
            ("de cuantos digitos es la contraseña", "digitos tiene la contraseña", "cantidad de digitos de la contraseña", DUDA_LONG, "tamaño contraseña") : "La contraseña tiene 6 dígitos",
            ("lo ultimo", "la ultima parte", "esto", "esta parte") : "Ahora lo repetimos",
            ("confirma la contraseña", "confirmar la contraseña"): "Para confirmar la contraseña tenés que escribirla una segunda vez, asegurate de que coincidan y continuá con el siguiente paso",            
            ("Cuál es el chip", "Cual es el chip", "Dónde está el chip?", "Donde está el chip?", "No veo el chip") : "Si te fijás, es el pequeño cuadradito de color plateado ¿Lo ves?",
            ("Ya está", "Ya esta", "Ya está listo", "Ya esta listo") : "Si, eso es todo"
        }

        for key in respuestasdudatuple.keys():
            if duda in key:
                message = respuestasdudatuple.get(key)
                dispatcher.utter_message(text=str(message))
                return[]

        message = "Cuál es tu duda?"
        dispatcher.utter_message(text=str(message))
       
        return []      

class ActionComenzarMicrotraining(Action):
    def name(self) -> Text:
        return "action_comenzar_microtraining"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        time.sleep(5)
        room_microlearning = str(tracker.get_slot("room_microlearning"))

        if(room_microlearning == "RoomBanco"):
            dispatcher.utter_message(text="Tomá tu tarjeta y fijate que tiene un chip. De ese lado, introducila en la boquilla iluminada de verde")
        
        return[]
