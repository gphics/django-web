import Link from "next/link";
import { IoLogoLinkedin } from "react-icons/io";
import { FaSquareGithub } from "react-icons/fa6";
function FooterComponent() {
  const linkedinUrl = "https://linkedin.com/in/abdulbasit-abdulhakeem-013a42213"
  const githubUrl = "https://github.com/gphics"
  return (
    <div className="flex bg-primary-color h-[40px] items-center justify-center text-off-white">
      <p>Developed by Abdulbasit</p>
      <section className="flex ml-1">

        <Link target="_blank" className="mx-2" href={linkedinUrl} ><IoLogoLinkedin className="size-6 hover:text-accent-color" /></Link>

        <Link target="_blank" href={githubUrl} ><FaSquareGithub className="size-6 hover:text-accent-color" /></Link>
      </section>
      
    </div>

  )
}

export default FooterComponent