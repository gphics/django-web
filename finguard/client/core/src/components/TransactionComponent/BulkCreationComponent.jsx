"use client"

import CookieManager from "@/utils/cookieManager"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { toast, ToastContainer } from "react-toastify"
import FullPageLoadingComponent from "../Others/FullPageLoadingComponent"

function BulkCreationComponent() {
  const [file, setFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const cookieMgt = CookieManager()
  const authToken = cookieMgt.getCookie()

  async function submitHandler(e) {
    e.preventDefault()

    if (!file) {
      toast.warning("a csv file must be uploaded")
    }
    setIsLoading(true)
    const formData = new FormData()
    formData.append("transaction_file", file)

    const url = process.env.NEXT_PUBLIC_SERVER_URL +"transaction/"

    const first = await fetch(url, { method: "POST", body: formData, headers: { "Authorization": "Token " + authToken } })
    const second = await first.json()
    setIsLoading(false)
    if (second?.err || !second?.success) {
      toast.error(second?.err[0])
      return
    }

    router.replace("/dashboard")
  }

  function onChangeHandler(e) {
    const uploadedFile = e.target.files?.[0]

    setFile(uploadedFile)
  }
  return (
    <div className='flex flex-col transition-all duration-300 px-1'>
      <ToastContainer />
      {!!isLoading && <FullPageLoadingComponent/>}
      <article className=''>
        <h2 className='poppins-bold text-[1.2em] my-1'>Format</h2>

        <p>Acceptable file format: csv format</p>
        <div>
          <h4 className='poppins-bold'>Columns:</h4>
          <ol className='relative left-5  w-fit'>
            <li> <strong>amount: </strong> number (integer | float) </li>
            <li> <strong>transaction_date:</strong>  datetime(e.g {new Date().toISOString()} )</li>
            <li><strong>description: </strong>text</li>
            <li><strong>transaction_type:</strong> text (DEBIT | CREDIT)</li>
            <li><strong>category:</strong> text (e.g Shopping) </li>
          </ol>
        </div>

      </article>

      <form onSubmit={submitHandler} className='flex flex-col mt-4'>
        <label htmlFor="transaction_file">Transaction File</label>
        <input onChange={onChangeHandler} className='bg-accent-color mt-2 w-50 w-max-[350px] rounded-sm h-[40px] px-1 pt-2 text-center cursor-pointer hover:bg-overlay' type="file" name="transaction_file" required accept=".csv, text/csv" />

        <button type="submit" className="bg-accent-color poppins-bold mt-3 w-fit px-3 py-1 rounded-sm ml-15 cursor-pointer">Submit</button>
      </form>
    </div>
  )
}

export default BulkCreationComponent