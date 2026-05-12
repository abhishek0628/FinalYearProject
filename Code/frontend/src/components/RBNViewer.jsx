import "../styles.css";
export default function RBNViewer({
    rbn
}) {

    return (

        <div className="card">

            <h2>
                RBN Encoding
            </h2>

            <h3>
                RC
            </h3>

            <pre>
                {
                    JSON.stringify(
                        rbn.RC,
                        null,
                        2
                    )
                }
            </pre>

            <h3>
                RL
            </h3>

            <pre>
                {
                    JSON.stringify(
                        rbn.RL,
                        null,
                        2
                    )
                }
            </pre>

            <h3>
                Sigma
            </h3>

            <pre>
                {
                    JSON.stringify(
                        rbn.Sigma,
                        null,
                        2
                    )
                }
            </pre>

            <h3>
                Unsafe States
            </h3>

            <pre>
                {
                    JSON.stringify(
                        rbn.unsafe_states,
                        null,
                        2
                    )
                }
            </pre>

        </div>
    );
}