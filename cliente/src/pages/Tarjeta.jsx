
const Tarjeta = ({ imagenSrc }) => {
  return (
    <div className="w-50 h-30 m-2 p-4 border-4 border-gray-500 rounded-lg text-center">
      <img src={imagenSrc} alt="Imagen" />
    </div>
  );
};

export default Tarjeta;
