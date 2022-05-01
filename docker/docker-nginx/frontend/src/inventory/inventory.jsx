import React, { useEffect, useState } from "react"

const UsingFetch = () => {
    const [inventory, setInventory] = useState([])

    const fetchData = () => {
        fetch("./inventory")
            .then(response => {
                return response.json()
            })
            .then(data => {
                setInventory(data)
            })
    }

    useEffect(() => {
        fetchData()
    }, [])

    const DisplayData = inventory.map(
        (server) => {
            return (
                <tr>
                    <td>{server.inventory_id}</td>
                    <td>{server.hname}</td>
                    <td>{server.appid}</td>
                </tr>
            )
        }
    )

    return (
        <div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Server</th>
                        <th>Application</th>
                    </tr>
                </thead>
                <tbody>


                    {DisplayData}

                </tbody>
            </table>

        </div>
    )
}



export default UsingFetch
