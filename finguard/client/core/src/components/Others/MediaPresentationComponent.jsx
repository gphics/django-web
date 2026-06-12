function MediaPresentationComponent({ media = null, name = "" }) {
    return <div>
        {media ? <></> : <h4 className="bg-accent-color text-white text-[1.2em] self-center text-center pt-[6px] w-10 h-10 rounded-sm mb-1 poppins-bold capitalize hover:shadow-md"> {name[0]} </h4>}
    </div>
}
  
export default MediaPresentationComponent