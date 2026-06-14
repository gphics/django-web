"use client"
import { toast, ToastContainer } from 'react-toastify'
import TransactionNavigator from './TransactionNavigator'
import TransactionListComponent from './TransactionListComponent'
import TransactionFilteringComponent from './TransactionFilteringComponent'
import { useEffect } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'


function TransactionRenderer({ result, currencyRes, filteringLimitRes }) {
  const { success, data = {}, err = null } = result || {}

  const searchParams = useSearchParams()
  const router = useRouter()
  const transactions = data?.transactions || []


  function toSummary() {
    router.push("/summary?" + searchParams.toString())
  }
  useEffect(() => {
    if (err) {
      toast.error(err[0], { toastId: "error-msg" })
    }
  }, [err])
  return (
    <div className='flex flex-col w-full'>
      {!success ? <h2 className='text-center poppins-bold text-[1.5em] text-rose-500 capitalize my-auto uppercase'> {err?.[0]}  </h2> :
        <>
          <ToastContainer theme='dark' position='top-center' />

          {/* Filtering component */}
          <TransactionFilteringComponent currencyRes={currencyRes} filteringLimitRes={filteringLimitRes} />

          {/* Transaction Creation */}
          <div className='my-2 mx-1 flex flex-col max-w-[500px] w-full self-center'>
            <section className='my-1 flex justify-between'>
              <Link className='bg-accent-color px-3 py-1 cursor-pointer hover:rounded-sm hover:poppins-bold hover:bg-emerald-400 transition-all duration-400' href={"/transaction/create"}>Create</Link>
              <button className='bg-accent-color px-3 py-1 cursor-pointer hover:rounded-sm hover:poppins-bold hover:bg-emerald-400 transition-all duration-400' onClick={toSummary}>Summarize</button>

            </section>
            <hr />
          </div>

 
          {/* Other Component */}

          <TransactionListComponent currencyRes={currencyRes} transactions={transactions} transactionCount={data?.count} />
          {transactions.length ? <TransactionNavigator current_page={data?.current_page || 1} total_pages={data?.total_pages || 1} /> : <></>}
        </>}
    </div>
  )
}


export default TransactionRenderer