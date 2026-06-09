import Image from "next/image"
import NotFoundImg from "../../public/imgs/not-found.jpg"
import Link from "next/link"

function NotFoundPage() {
  return (
      <div className="flex-auto flex flex-col justify-center items-center">
          <Image src={NotFoundImg} alt="not found image" className="max-sm:size-auto" priority="eager" height={400}  />

          <Link href={"/"} className="bg-accent-color px-3 py-2 rounded-md poppins-bold transition-transform duration-100 hover:scale-[1.05]">Back Home</Link>
    </div>
  )
}

export default NotFoundPage