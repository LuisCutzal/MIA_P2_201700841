import Consola from "./Consola"
import Encabezado from "./Encabezado"
import { useState } from "react"

function Home() {
    const [contenido, setContenido] = useState("")
    const [contenidoConsola, setContenidoConsola] = useState("")

    const handleClickEjecutar = () => {
        //setContenidoConsola(contenido)
        const requestOpcions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entry: contenido })
        };
        //ahora realizaremos la solicitud post al servidor flask
        fetch("http://127.0.0.1:5000/api", requestOpcions)
            .then(Response => Response.json())
            .then(data =>{
                //actualizamos el estado de la segunda consola con la respuesta del servidor
                var valorMensaje = ""
                for(var text in data.salida){
                    valorMensaje += data.salida[text]+'\n'
                }
                setContenidoConsola(valorMensaje);
            })
            .catch(error =>{
                console.error("Error al ejecutar la solicitud POST:", error);
            });
    };

    return (
        <div className="h-full w-full flex flex-col gap-5">
            <Encabezado Contenido={setContenido} Ejecutar = {handleClickEjecutar} />
            <Consola contenido={contenido} Contenido={setContenido}/>
            <Consola contenido = {contenidoConsola} esEditable={false}/>
        </div>
    )
}
export default Home


/* 
import Consola from "./Consola"
import Encabezado from "./Encabezado"
import { useState } from "react"

function Home() {
    const [contenido, setContenido] = useState("")
    const [contenidoConsola, setContenidoConsola] = useState("")

    const handleClickEjecutar = () => {
        setContenidoConsola(contenido)
    }

    return (
        <div className="h-full flex flex-col gap-5">
            <Encabezado Contenido={setContenido} Ejecutar = {handleClickEjecutar} />
            <Consola contenido={contenido} Contenido={setContenido}/>
            <Consola contenido = {contenidoConsola} esEditable={false}/>
        </div>
    )
}
export default Home

*/