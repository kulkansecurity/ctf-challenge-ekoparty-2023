        const params = new URLSearchParams(window.location.search);
	document.getElementById('input_json').value = params.get('input_json') || '';

        let randomObject = {};
 
        function mergeObjects(target, source) {
            for (let key in source) {
                if (typeof source[key] === 'object' && source[key] !== null) {
                    if (!target[key]) {
                        target[key] = {};
                    }
                    mergeObjects(target[key], source[key]);
                } else {
                    target[key] = source[key];
                }
            }
        }
 
        function applyUpdate() {
            const configStr = document.getElementById('input_json').value;
            let config = {};
 
            try {
                config = JSON.parse(configStr);
            } catch (e) {
                console.log("Invalid JSON, you can do better for Messi.");
                return;
            }

	    // Hey, you're doing a great job if you're here reviewing code. You've got this!
            let defaultConfig = { color: "blue", fontSize: "16px" };
            mergeObjects(defaultConfig, config);
 
            const complimentDiv = document.getElementById('compliment');
 
            if (defaultConfig.compliment) {
                complimentDiv.innerText = defaultConfig.compliment;
            }
            if (defaultConfig.color) {
                complimentDiv.style.color = defaultConfig.color;
            }
            if (defaultConfig.fontSize) {
                complimentDiv.style.fontSize = defaultConfig.fontSize;
            }
            if (randomObject.win) {
                complimentDiv.innerHTML = randomObject.win;
            }
        }


	applyUpdate();
