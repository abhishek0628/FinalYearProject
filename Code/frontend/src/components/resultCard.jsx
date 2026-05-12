import "../styles.css";
export default function ResultCard({
    safe,
    unsafe
}) {

    return (

        <div className={safe ? "safe" : "unsafe"}>

            <h2>
                {
                    safe
                        ? "✅ SYSTEM IS SAFE"
                        : "❌ UNSAFE STATE REACHED"
                }
            </h2>

            {
                !safe && (
                    <pre>
                        {
                            JSON.stringify(
                                unsafe,
                                null,
                                2
                            )
                        }
                    </pre>
                )
            }

        </div>
    )
}