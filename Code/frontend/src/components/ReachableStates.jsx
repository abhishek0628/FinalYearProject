import "../styles.css";
export default function ReachableStates({
    states
}) {

    return (

        <div className="card">

            <h2>
                Reachable States
            </h2>

            {
                states.length === 0
                    ? (
                        <p>
                            No reachable states
                        </p>
                    )
                    : (
                        states.map(
                            (s, index) => (

                                <div
                                    key={index}
                                    className="state-box"
                                >

                                    <p>

                                        <strong>
                                            Agents:
                                        </strong>

                                        {
                                            " "
                                        }

                                        {
                                            s.agents.join(", ")
                                        }

                                    </p>

                                    <p>

                                        <strong>
                                            Environment:
                                        </strong>

                                        {
                                            " "
                                        }

                                        {
                                            s.env
                                        }

                                    </p>

                                </div>
                            )
                        )
                    )
            }

        </div>
    );
}