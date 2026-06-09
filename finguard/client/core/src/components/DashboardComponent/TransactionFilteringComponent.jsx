"use client"
import { FaArrowUp, FaArrowDown } from "react-icons/fa";
import { useRouter, useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { toast } from 'react-toastify'

function TransactionFilteringComponent({ filteringLimitRes, currencyRes }) {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [showFilter, setShowFilter] = useState(false)
  const {page, ...currentFilters} = Object.fromEntries(searchParams.entries())
  
 const [filters, setFilters] = useState({ ...currentFilters })
  const { data = {}, err = null } = filteringLimitRes
  useEffect(() => {
    if (err) {
      toast.error(err[0], { toastId: "error-msg" })
    }
  }, [err])

 
  const currency = currencyRes?.data?.msg?.currency || "$"

  function InputOnChangeHandler(e) {
    const { value, name } = e.target

    const newFilters = { ...filters }

    if (value === "" || value === 0) {
      delete newFilters[name]
    } else {

      newFilters[name] = value
    }
    setFilters(newFilters)
  }

  const  msg = data?.msg || {}
  const rangeFilters = [
    {
      name: "min_amount",
      title: "Minimum Amount(" + currency + ")",
      min: msg?.min_amount,
      max: msg?.max_amount + 2000,
      value: filters?.min_amount || 0
    },
    {
      name: "max_amount",
      title: "Maximum Amount(" + currency + ")",
      min: msg?.min_amount,
      max: msg?.max_amount + 2000,
      value: filters?.max_amount || 0
    },
    {
      name: "min_year",
      title: "Minimum Year",
      min: msg?.min_year,
      max: msg?.max_year + 10,
      value: filters?.min_year || new Date().getFullYear()
    },
    {
      name: "max_year",
      title: "Maximum Year",
      min: msg?.min_year,
      max: msg?.max_year + 10,
      value: filters?.max_year || new Date().getFullYear()
    },
    {
      name: "min_month",
      title: "Minimum Month",
      min: 1,
      max: 12,
      value: filters?.min_month || new Date().getMonth() + 1
    },
    {
      name: "max_month",
      title: "Maximum Month",
      min: 1,
      max: 12,
      value: filters?.max_month || new Date().getMonth() + 1
    },
  ]
  

  const selectFilters = [
    {
      name: "category",
      title: "Category",
      value: filters?.category || "",
      options: [...msg?.categories || []],
      placeholder: "Select a category"
    },
    {
      name: "transaction_type",
      title: "Transaction Type",
      value: filters?.transaction_type || "",
      options: [...msg?.transaction_type || []],
      placeholder: "Select type"
    },
  ]

  function resetFilters() {
    setFilters({})
    router.push("/dashboard")
  }

  function applyFilters() {
    const params = new URLSearchParams(filters)
    router.push("/dashboard?" + params.toString())
  }
  return (
    <div className='flex flex-col my-2 justify-start shadow-md'>

      {/* filter display */}
      <div className="self-end flex items-center justify-end border-b border-b-4 w-fit mb-2">
        <span className="mr-4 cursor-pointer">{showFilter ? <FaArrowUp onClick={(e) => setShowFilter(prev => !prev)} /> : <FaArrowDown onClick={(e) => setShowFilter(prev => !prev)} />} </span>
        <h3 className='poppins-bold w-fit p-1'>Filter </h3>

      </div>

      {showFilter &&
        <main className="transition-all">
          {/* filters */}
          <div className='flex flex-col'>

            {/* Range Filters */}
            <section className='self-center my-1 flex flex-wrap justify-around items-center max-md:flex-col w-[90%]'>
              {rangeFilters.map((elem, index) => {
                return <div key={index} className='m-2 h-15 items-center  flex flex-col'>
                  <label htmlFor={elem.name}> {elem.title}  </label>
                  <input onChange={InputOnChangeHandler} value={elem.value} type="range" name={elem.name} min={elem.min} max={elem.max} />
                  <small className='block'> {elem.value} </small>
                </div>
              })}
            </section>

            {/* Select Filters */}
            <section className='self-center my-1 flex flex-wrap justify-around items-center max-md:flex-col w-[90%]'>
              {selectFilters.map((elem, index) => {
                return <div key={index} className='m-2 h-15 items-center  flex flex-col'>
                  <label htmlFor={elem.name}> {elem.title} </label>
                  <select onChange={InputOnChangeHandler} value={elem.value} name={elem.name}>
                    <option value="">  {elem.placeholder} </option>
                    {elem.options.map((opt, i) => {
                      return <option key={i} value={opt}> {opt}  </option>
                    })}
                  </select>
                </div>
              })}
              {/* selection input for flagged */}
              <div className='m-2 h-15 items-center  flex flex-col'>
                <label htmlFor="flagged">Flagged</label>
                <select onChange={InputOnChangeHandler} value={filters?.flagged || ""} name="flagged">
                  <option value="">Select</option>
                  <option value={false}>False</option>
                  <option value={true}>True</option>
                </select>
              </div>
            </section>
          </div>



          {/* control */}
          <section className='flex justify-center my-2'>
            <button onClick={resetFilters} type="button" className='bg-rose-400 mx-3 py-1 px-4 poppins-bold cursor-pointer hover:rounded-sm hover:bg-rose-600 hover:text-white transition-all duration-500'>Reset</button>


            <button type="button" className='bg-emerald-400 mx-3 py-1 px-4 poppins-bold cursor-pointer hover:rounded-sm hover:bg-emerald-600 hover:text-white transition-all duration-500' onClick={applyFilters}>Apply</button>
          </section>
        </main>
      }
    </div>
  )
}

export default TransactionFilteringComponent