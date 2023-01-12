const createNode = (tag, attributes, innerHTML) => {
	let node = document.createElement(tag);
	for (const [attribute, value] of Object.entries(attributes)) {
		node.setAttribute(attribute, value);
	}
	if (typeof innerHTML == "string") {
		node.innerHTML = innerHTML;
	} else if (Array.isArray(innerHTML)) {
		for (const child of innerHTML) {
			if (typeof child == "string") {
				const textElement = document.createTextNode(child);
				node.appendChild(textElement);
			} else {
				node.appendChild(child);
			}
		}
	}
	return node;
}

export {
	createNode
}