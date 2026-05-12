import "../styles.css";
export default function LogsPanel({
    logs
}) {

    return (

        <div className="card">

            <h2>
                Execution Logs
            </h2>

            <pre className="logs">

                {
                    logs
                }

            </pre>

        </div>
    );
}