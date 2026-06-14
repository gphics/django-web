"use client"

import Link from "next/link"
import { toast } from "react-toastify"
import MediaPresentationComponent from "../Others/MediaPresentationComponent"

function CircleListComponent({ circleRes }) {

  if (circleRes?.err || !circleRes?.success) {

    toast.error(circleRes?.err[0])
  }
  const data = circleRes?.data?.msg || []
  
  return <>
    {!!data?.length && data?.map((elem, i) => {

      return <Link key={i} href={"/circle/"+elem?.id} className="w-[150px] flex flex-col justify-center items-center p-3 bg-overlay m-1 hover:bg-accent-color transition-all duration-300"> 
        <MediaPresentationComponent media={elem?.media} name={elem?.name}  />
        <h4 className="text-[0.9em] mb-1 text-center my-1"> <strong>{elem?.name.length <= 20 ? elem?.name : elem?.name.slice(0, 20) +".."}  </strong>  </h4>
        <h5 className="text-[0.8em]"> {elem.members?.length} Member(s) </h5>
      </Link>
    })}
  </>

}


export default CircleListComponent