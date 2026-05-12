export default function InputPanel({
    input,
    setInput,
    runCheck,
    loading
}) {

    // =====================================
    // FILE UPLOAD
    // =====================================

    const handleFileUpload = (e) => {

        const file = e.target.files[0];

        if (!file) {
            return;
        }

        const reader = new FileReader();

        reader.onload = (event) => {

            setInput(event.target.result);
        };

        reader.readAsText(file);
    };

    return (

        <div className="card">

            <h2>
                OMAS Input
            </h2>

            {/* FILE UPLOAD */}

            <input
                type="file"
                accept=".txt"
                onChange={handleFileUpload}
            />

            <br />
            <br />

            {/* TEXTAREA */}

            <textarea
                value={input}
                onChange={(e) =>
                    setInput(e.target.value)
                }
                placeholder="Paste OMAS model here..."
            />

            {/* BUTTON */}

            <button
                onClick={runCheck}
                disabled={loading}
            >

                {
                    loading
                        ? "Checking..."
                        : "Run Safety Check"
                }

            </button>

        </div>
    );
}