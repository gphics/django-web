"use client"

function InputComponent({ onChangeHandler, value, name, type = "text", label = null, Icon = null , others={}}) {
    return (
        <div className="flex flex-col my-4 w-[95%]">
            {label && <label htmlFor={name}>  {label} </label>}
            <section className="flex justify-between items-center  rounded-md  h-11 shadow-xl">
                {Icon && <Icon className="mx-1 size-5 text-accent-color" />}
                <input {...others} className="flex-auto text-off-white pl-2  rounded-md outline-none h-full" type={type} name={name} value={value} onChange={onChangeHandler} placeholder={name} />
            </section>

        </div>
    )
}

export default InputComponent