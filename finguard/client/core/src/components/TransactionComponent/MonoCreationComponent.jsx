"use client"
import { FaSearch } from "react-icons/fa";
import sendRequest from "@/utils/requestSender"
import { useState } from "react"
import { toast, ToastContainer } from "react-toastify"
import { useRouter } from "next/navigation";
import FullPageLoadingComponent from "../Others/FullPageLoadingComponent";

// amount, transaction_date, transaction_type, category

function MonoCreationComponent({ currency, transactionData = null }) {

    function dateProcessor(dateStr) {
        const proc = dateStr ? new Date(dateStr) : new Date()
        const lastProc = proc.toISOString().slice(0, 16)
        return lastProc
    }

    const router = useRouter()


    const [isLoading, setIsLoading] = useState(false)
    const [isSearching, setIsSearching] = useState(false)
    const [noMatching, setNoMatching] = useState(!transactionData)

    const [categories, setCategories] = useState([])

    function generateBasicData() {

        const basalData = { amount: "", transaction_date: dateProcessor(), transaction_type: "DEBIT", category: "", description: "" }

        // filling the data if update ...
        if (transactionData) {

            // filling ...
            basalData.amount = transactionData?.amount
            basalData.category = transactionData?.category
            basalData.description = transactionData?.description
            basalData.transaction_type = transactionData?.transaction_type
            basalData.transaction_date = dateProcessor(transactionData?.transaction_date)

            // setting noMatching ...
            // setNoMatching(false)
        }

        return basalData
    }

    // transaction data
    const [data, setData] = useState(generateBasicData())

    function onChangeHandler(e) {
        const { value, name } = e.target
        setData(prev => ({ ...prev, [name]: value }))
    }

    /**
     * 
     * @param {string} title 
     * This function fetch categories thar match the seach (title) word provided
     * 
     */
    async function fetchCategory(title) {
        if (!title) {
            toast.warn("category title must be provided")

            return
        }
        setIsSearching(true)

        const url = "transaction/category?title=" + title
        const res = await sendRequest(url)
        setIsSearching(false)
        if (!res.success) {
            toast.error(res?.err[0])
            return
        }
        const first = res?.data?.msg.map(elem => elem?.title)
        if (first.length) {
            setNoMatching(false)
        } else {
            setNoMatching(true)
        }
        setCategories(first)

    }

    function validateData() {
        let result = true
        const newData = { ...data }
        const dataArr = (Object.entries(newData))

        // looping ...
        dataArr.forEach(elem => {
            const key = elem[0]
            const value = elem[1]

            if (!value && key !== "description") {

                toast.warn(key + " must be provided", { toastId: key })
                result = false
            }
        })

        return result
    }

    async function submitHandler(e) {
        e.preventDefault()


        // validating the data
        const validationResult = validateData()

        // stop the process
        if (!validationResult) return;

        setIsLoading(true)

        const isUpdate = !!transactionData

        const url = isUpdate ? ("transaction/?id=" + transactionData?.id) : "transaction/"

        const body = { ...data, transaction_date: new Date(data?.transaction_date).toISOString() }

        const res = await sendRequest(url, { body, method: transactionData ? "PUT" : "POST" })
        setIsLoading(false)
        // if the process is unsuccessful
        if (res?.err || !res?.success) {
            toast.error(res?.err[0])
            return
        }

        // if process is successful
        router.replace("/dashboard")
    }
    return (
        <form onSubmit={submitHandler} className=' mx-auto flex flex-col transition-all duration-300 items-center w-full max-w-[400px]'>
            {!!isLoading && <FullPageLoadingComponent />}
            <ToastContainer theme="dark" position="top-center" />
<h2 className="font-bold text-[1.1em] uppercase my-2 text-center">Create Transaction</h2>
            {/* Amount */}
            <div className="flex flex-col my-1 w-[90%]">
                <label htmlFor="amount" className="font-medium">Amount({currency}) </label>
                <input className="bg-primary-color text-white rounded-sm px-2 h-[45px] my-1 border-none outline-none font-medium focus:bg-accent-color focus:text-primary-color" onChange={onChangeHandler} value={data?.amount} type="number" name="amount" />
            </div>

            {/* Transaction Date */}
            <div className="flex flex-col my-1 w-[90%]">
                <label htmlFor="transaction_date">Transaction Date</label>
                <input className="bg-primary-color text-white rounded-sm px-2 h-[45px] my-1 border-none outline-none font-medium focus:bg-accent-color focus:text-primary-color" onChange={onChangeHandler} value={data?.transaction_date} type="datetime-local" name="transaction_date" />
            </div>

            {/* Transaction Type */}
            <div className="flex flex-col my-1 w-[90%]">
                <label htmlFor="transaction_type">Transaction Type</label>
                <select className="bg-primary-color text-white rounded-sm px-2 h-[45px] my-1 border-none outline-none font-medium focus:bg-accent-color focus:text-primary-color" onChange={onChangeHandler} value={data?.transaction_type} name="transaction_type" id="">
                    <option value="DEBIT">DEBIT</option>
                    <option value="CREDIT">CREDIT</option>
                </select>
            </div>
            {/* Description */}
            <div className="flex flex-col my-1 w-[90%]">
                <label htmlFor="description">Description</label>
                <textarea className="py-2 bg-primary-color text-white rounded-sm px-2 h-[45px] my-1 border-none outline-none font-medium focus:bg-accent-color focus:text-primary-color field-sizing-content" name="description" placeholder="transaction description ..." onChange={onChangeHandler} value={data?.description} />
            </div>


            {/* Category ... */}
            <div className="flex flex-col my-1 w-[90%]">
                <label htmlFor="category">Category</label>
                <section className=" flex justify-between">
                    <input onChange={(e) => {
                        onChangeHandler(e)
                        setNoMatching(false)

                    }} placeholder="category title ..." type="search" className="bg-primary-color text-white rounded-l-sm px-2 h-[45px] my-1 border-none outline-none font-medium focus:bg-accent-color focus:text-primary-color flex-auto" name="category" value={data?.category} />
                    <button onClick={() => { fetchCategory(data?.category) }} className="bg-overlay h-[45px] self-center px-2 ml-1 cursor-pointer hover:bg-accent-color rounded-r-sm" type="button"><FaSearch /></button>
                </section>

                {/* listing category search result */}
                {!noMatching ?

                    <article className="flex flex-wrap justify-around  mt-2">


                        {categories.map((elem, i) => {

                            return <p className={`my-1  mx-1 w-fit px-2 cursor-pointer transition-all duration-300 hover:bg-accent-color ${elem === data?.category ? "bg-accent-color" : "bg-overlay "}`}
                                key={i} onClick={(e) => {

                                    setData(prev => ({ ...prev, category: elem }))
                                }}> {elem}</p>
                        })}
                    </article>
                    : <>
                        {/* first info */}
                        {isSearching ? <h4 className="poppins-bold  text-center my-1">searching ...</h4> : <></>}

                        {/* second info */}
                        {noMatching && data?.category ? <h4 className="poppins-bold   text-center my-1"> New category {`"${data?.category}"`} will be created when you submit the form.</h4> : <></>}
                    </>}
            </div>




            {/* submit */}
            <button className="bg-accent-color w-fit self-center px-3 py-1 poppins-bold rounded-sm my-5 cursor-pointer transition-all duration-300 hover:scale-[1.02]" type="submit">Submit</button>
        </form>
    )
}

export default MonoCreationComponent