// eslint-disable-next-line react/prop-types
function Consola({contenido, Contenido, esEditable = true}){
    //primero es el valor, segundo es funcion
    // const [contenidoTextArea, setContenidoTextArea] = useState("");

    const handleTextAreaChange = (e) => {
        const nuevoContenido = e.target.value;
        Contenido(nuevoContenido)
    }

    return(
        <div className=" h-1/2 p-2">
            <textarea className="w-full h-full resize-none bg-black text-white p-3"
            value={contenido}
            onChange={handleTextAreaChange}
            readOnly={esEditable ? false : true}
            ></textarea>
        </div>
    )
}
export default Consola;