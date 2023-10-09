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