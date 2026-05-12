import React, { useState } from "react";

import API from "./services/api";

import InputPanel from "./components/InputPanel";
import ResultCard from "./components/resultCard";
import ReachableStates from "./components/ReachableStates";
import RBNViewer from "./components/RBNViewer";
import LogsPanel from "./components/LogsPanel";

import "./styles.css";


export default function App() {

    const [input, setInput] = useState("");

    const [loading, setLoading] = useState(false);

    const [result, setResult] = useState(null);


    // =====================================
    // RUN CHECK
    // =====================================

    const runCheck = async () => {

        try {

            setLoading(true);

            const res = await API.post(
                "/check",
                {
                    input
                }
            );

            setResult(res.data);

        } catch (err) {

            console.error(err);

        } finally {

            setLoading(false);
        }
    };


    // =====================================
    // UI
    // =====================================

    return (

        <div className="container">

            <h1>
                OMAS Safety Checker
            </h1>

            <InputPanel
                input={input}
                setInput={setInput}
                runCheck={runCheck}
                loading={loading}
            />

            {
                result && (
                    <>

                        <ResultCard
                            safe={result.safe}
                            unsafe={result.unsafe_reached}
                        />

                        <ReachableStates
                            states={result.reachable_states}
                        />

                        <RBNViewer
                            rbn={result.rbn}
                        />

                        <LogsPanel
                            logs={result.logs}
                        />

                    </>
                )
            }

        </div>
    );
}