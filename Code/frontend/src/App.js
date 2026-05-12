import React, { useState } from "react";

import API from "./services/api";

import InputPanel from "./components/input";
import ResultCard from "./components/results";
import ReachableStates from "./components/reachablestates";
import RBNViewer from "./components/rbnviewer";
import LogsPanel from "./components/logs";

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