"use client"
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";
import { useRouter, useSearchParams } from "next/navigation"

/**
 * This component is responsible for fetching new transactions
 * @param {{total_pages:number, current_page:number}} param0 
 */
function TransactionNavigator({ total_pages, current_page }) {
    const router = useRouter()
    const searchParams = useSearchParams()
    const { page, ...currentParams } = Object.fromEntries(searchParams.entries())
    const paramString = new URLSearchParams(currentParams).toString()
    function previousBtnHandler(e) {
        const transCurrentPage = +current_page
        const newPage = transCurrentPage === 1 ? total_pages : transCurrentPage - 1

        // redirecting
        router.push("/dashboard/?page=" + newPage+"&" + paramString)
    }
    function nextBtnHandler(e) {
        const transCurrentPage = +current_page
        const transTotalPages = +total_pages
        const newPage = transCurrentPage === transTotalPages ? 1 : transCurrentPage + 1

        // redirecting
        router.push("/dashboard/?page=" + newPage+"&" + paramString)
    }
    return <section className="flex justify-center items-center my-2 transition-colors duration-400">
        <button className="bg-gray-400 rounded-full p-3 poppins-bold mr-2 cursor-pointer hover:bg-accent-color transition-colors duration-400 hover:text-white" onClick={previousBtnHandler} type="button">
            <FaArrowLeft/>
        </button>
        <p>Page {current_page} of {total_pages}  </p>
        <button className="bg-gray-400 rounded-full p-3 poppins-bold ml-2 cursor-pointer hover:bg-accent-color transition-colors duration-400 hover:text-white" onClick={nextBtnHandler} type="button">
            <FaArrowRight />
        </button>
    </section>
}

export default TransactionNavigator