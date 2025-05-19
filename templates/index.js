
    document.addEventListener('DOMContentLoaded', function () {
        const fromScratchRadio = document.getElementById('fromScratch');
        const fromMiddleRadio = document.getElementById('fromMiddle');
        const middleInput = document.getElementById('middleNumInputs');

        // Function to toggle visibility
        function toggleMiddleInput() {
            if (fromMiddleRadio.checked) {
                middleInput.style.display = 'block';
            } else {
                middleInput.style.display = 'none';
            }
        }

        // Initial hide (in case it's not already hidden)
        toggleMiddleInput();

        // Add event listeners
        fromScratchRadio.addEventListener('change', toggleMiddleInput);
        fromMiddleRadio.addEventListener('change', toggleMiddleInput);
    });
