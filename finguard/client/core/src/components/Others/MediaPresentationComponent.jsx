"use client"
import Image from "next/image"

function MediaPresentationComponent({ media = null, name = "" }) {
    
    return <div className="my-2" >
        {media ? <Image className="object-cover aspect-square rounded-full border-2 border-accent-color" height={70} width={70} src={media?.public_url} alt="media" /> : <h4 className="bg-accent-color text-white text-[1.5em] font-bold self-center text-center pt-[15px] w-[70px] h-[70px] rounded-full mb-1 poppins-bold capitalize hover:shadow-md border-2 border-accent-color"> {name[0]} </h4>}
    </div>
}

export default MediaPresentationComponent