"use client"

import CookieManager from "@/utils/cookieManager"
import Logo from "../../public/logo/full-logo-horizontal.svg"
import Image from 'next/image'
import Link from 'next/link'
import { usePathname, useRouter } from "next/navigation"
import { FaBars } from "react-icons/fa";
function NavigationComponents() {
    const pathname = usePathname()
    const isAuthOrHome = pathname === "/" || pathname.startsWith("/auth")
    return isAuthOrHome ? <NonAuthNav /> : <AuthNavComponent />

}


function AuthNavComponent() {
    const router = useRouter()
    const linkArr = [
        "dashboard",
        "profile",
        "circle",
        "summary"
    ]
    function btnClick(e) {
        const elem = document.querySelector("#nav-holder")
        elem.classList.toggle("toggle-show")
    }

    function logoutAction(e) {
        const cookieMgt = CookieManager()
        cookieMgt.deleteCookie()
        router.replace("/")
    }
    return <div>
        {/* bar click */}
        <section className="md:hidden my-1 z-10 pl-1 transition-all duration-300">
            <button onClick={btnClick} className="text-accent-color text-center hover:text-primary-color cursor-pointer"> <FaBars className="size-8"/> </button>
        </section>

        {/* all links */}
        <section id="nav-holder" className='flex justify-between items-center px-2 py-3 mb-2 max-md:absolute bg-white w-[100%] max-md:translate-x-[-100%] transition-transform duration-500 max-md:flex-col max-md:items-start shadow-xl'>
            <Link href="/" className="hover:transform-[scale(1.02)]">
                <Image src={Logo} alt="logo" loading={"eager"} height={30} />
            </Link>
            <section className="w-[65%] flex justify-around max-md:flex-col flex-auto">
                {linkArr.map((elem, index) => {
                    return <Link onClick={btnClick} className="capitalize hover:poppins-bold px-2 py-1 hover:bg-accent-color w-fit " href={"/" + elem} key={index}> {elem} </Link>
                })}
            </section>
            <button onClick={logoutAction} type='button' className="px-3 py-1 bg-accent-color poppins-bold rounded-sm cursor-pointer hover:text-white max-md:mb-5">Logout</button>
        </section>


    </div>
}

function NonAuthNav(params) {
    return <div className='flex justify-between items-center px-2 py-1 mb-2'>



        <Link href="/">
            <Image src={Logo} alt="logo" loading={"eager"} height={30} />
        </Link>
        <Link href={"/auth/register"} className='bg-accent-color text-white rounded-sm text-center px-3 py-1 poppins-bold'>Get Started</Link>

    </div>
}
export default NavigationComponents