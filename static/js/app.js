let products = [];

document.addEventListener("DOMContentLoaded", () => {
    loadProducts();
    loadOrders();
});

function showPanel(panelId) {
    document.querySelectorAll('.panel').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-buttons button').forEach(el => el.classList.remove('active'));
    
    const panel = document.getElementById(panelId);
    if(panel) panel.classList.add('active');
    
    // Find the button that was clicked
    const clickedBtn = Array.from(document.querySelectorAll('.nav-buttons button')).find(btn => btn.getAttribute('onclick').includes(panelId));
    if(clickedBtn) clickedBtn.classList.add('active');
}

function searchProducts() {
    const query = document.getElementById('productSearch').value.toLowerCase();
    const rows = document.querySelectorAll('#productsTableBody tr');
    
    rows.forEach(row => {
        const productName = row.cells[1].innerText.toLowerCase();
        if (productName.includes(query)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });

    // Also filter the "New Order" dropdowns if they are open
    updateOrderProductDropdowns(query);
}

// --- PRODUCT MANAGEMENT ---

function loadProducts() {
    fetch('/getProducts')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            products = data.products;
            const tbody = document.getElementById('productsTableBody');
            tbody.innerHTML = '';
            
            products.forEach(p => {
                tbody.innerHTML += `
                    <tr>
                        <td>${p.product_id}</td>
                        <td>${p.name}</td>
                        <td>${p.unit}</td>
                        <td>₹${parseFloat(p.price_per_unit).toFixed(2)}</td>
                        <td><button class="btn-danger" onclick="deleteProduct(${p.product_id})">Delete</button></td>
                    </tr>
                `;
            });
            
            // Also update any existing dropdowns in the order form
            updateOrderProductDropdowns();
        })
        .catch(err => console.error("Error loading products:", err));
}

function addProduct() {
    const name = document.getElementById('productName').value;
    const unit = document.getElementById('productUnit').value;
    const price = document.getElementById('productPrice').value;

    if (!name || !price) {
        alert("Please specify name and price.");
        return;
    }

    fetch('/insertProduct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, unit: unit, price_per_unit: parseFloat(price) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            // Clear inputs
            document.getElementById('productName').value = '';
            document.getElementById('productPrice').value = '';
            loadProducts();
        }
    });
}

function deleteProduct(id) {
    if(!confirm("Are you sure you want to delete this product?")) return;
    fetch('/deleteProduct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: id })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) alert("Error: " + data.error);
        loadProducts();
    });
}

// --- ORDER MANAGEMENT ---

function loadOrders() {
    fetch('/getOrders')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            const tbody = document.getElementById('ordersTableBody');
            tbody.innerHTML = '';
            data.orders.forEach(o => {
                const date = new Date(o.date).toLocaleString();
                tbody.innerHTML += `
                    <tr>
                        <td>#${o.order_id}</td>
                        <td>${o.customer_name}</td>
                        <td style="color: var(--success); font-weight: bold;">₹${parseFloat(o.total).toFixed(2)}</td>
                        <td>${date}</td>
                    </tr>
                `;
            });
        })
        .catch(err => console.error("Error loading orders:", err));
}

function addOrderRow() {
    const tbody = document.getElementById('orderRows');
    const rowId = 'row_' + Date.now();
    
    let options = `<option value="">Select Product...</option>`;
    products.forEach(p => {
        options += `<option value="${p.product_id}" data-price="${p.price_per_unit}">${p.name}</option>`;
    });

    const tr = document.createElement('tr');
    tr.id = rowId;
    tr.innerHTML = `
        <td>
            <select class="product-select" onchange="updateRowPrice('${rowId}')">${options}</select>
        </td>
        <td><span class="price-val">₹0.00</span></td>
        <td><input type="number" min="1" value="1" style="width: 80px;" onchange="calculateRowTotal('${rowId}')"></td>
        <td><span class="total-val">₹0.00</span></td>
        <td><button class="btn-danger" onclick="removeOrderRow('${rowId}')">✕</button></td>
    `;
    tbody.appendChild(tr);
}

function updateOrderProductDropdowns(filterQuery = "") {
    const selects = document.querySelectorAll('.product-select');
    selects.forEach(select => {
        const currentVal = select.value;
        let options = `<option value="">Select Product...</option>`;
        products.forEach(p => {
            if (!filterQuery || p.name.toLowerCase().includes(filterQuery)) {
                options += `<option value="${p.product_id}" data-price="${p.price_per_unit}">${p.name}</option>`;
            }
        });
        select.innerHTML = options;
        select.value = currentVal;
    });
}

function updateRowPrice(rowId) {
    const row = document.getElementById(rowId);
    const select = row.querySelector('.product-select');
    const selectedOption = select.options[select.selectedIndex];
    
    if (selectedOption.value !== "") {
        const price = parseFloat(selectedOption.getAttribute('data-price'));
        row.querySelector('.price-val').innerText = `₹${price.toFixed(2)}`;
    } else {
        row.querySelector('.price-val').innerText = `₹0.00`;
    }
    calculateRowTotal(rowId);
}

function calculateRowTotal(rowId) {
    const row = document.getElementById(rowId);
    const select = row.querySelector('.product-select');
    const selectedOption = select.options[select.selectedIndex];
    
    if (selectedOption.value !== "") {
        const price = parseFloat(selectedOption.getAttribute('data-price'));
        const qty = parseFloat(row.querySelector('input').value) || 0;
        const total = price * qty;
        row.querySelector('.total-val').innerText = `₹${total.toFixed(2)}`;
    } else {
        row.querySelector('.total-val').innerText = `₹0.00`;
    }
    calculateGrandTotal();
}

function calculateGrandTotal() {
    let grandTotal = 0;
    document.querySelectorAll('#orderRows tr').forEach(row => {
        const totalText = row.querySelector('.total-val').innerText.replace('₹', '');
        grandTotal += parseFloat(totalText) || 0;
    });
    document.getElementById('grandTotal').innerText = `₹${grandTotal.toFixed(2)}`;
    return grandTotal;
}

function removeOrderRow(rowId) {
    document.getElementById(rowId).remove();
    calculateGrandTotal();
}

function submitOrder() {
    const customerName = document.getElementById('customerName').value;
    if (!customerName) {
        alert("Please enter customer name.");
        return;
    }

    const orderItems = [];
    document.querySelectorAll('#orderRows tr').forEach(row => {
        const select = row.querySelector('.product-select');
        const qty = row.querySelector('input').value;
        const totalText = row.querySelector('.total-val').innerText.replace('₹', '');
        
        if (select.value) {
            orderItems.push({
                product_id: parseInt(select.value),
                quantity: parseFloat(qty),
                price_per_unit: parseFloat(select.options[select.selectedIndex].getAttribute('data-price')),
                total: parseFloat(totalText)
            });
        }
    });

    if (orderItems.length === 0) {
        alert("Please add at least one product to the order.");
        return;
    }

    const grandTotal = calculateGrandTotal();

    const orderPayload = {
        customer_name: customerName,
        total: grandTotal,
        order_items: orderItems
    };

    fetch('/insertOrder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderPayload)
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            alert("Error: " + data.error);
        } else {
            alert("Order completed successfully! Order ID: " + data.order_id);
            // Reset form
            document.getElementById('customerName').value = '';
            document.getElementById('orderRows').innerHTML = '';
            document.getElementById('grandTotal').innerText = '$0.00';
            loadOrders();
            // Programmatically return to dashboard
            document.querySelector('.nav-buttons button:nth-child(1)').click();
        }
    });
}

// --- AI PREDICTION ---

function predictSales() {
    const resultElement = document.getElementById('predictionResult');
    resultElement.innerText = "Processing...";
    
    fetch('/predictSales')
        .then(response => response.json())
        .then(data => {
            if (data.predicted_sales > 0) {
                resultElement.innerText = `₹${parseFloat(data.predicted_sales).toFixed(2)}`;
            } else {
                resultElement.innerText = "Need details/More Data";
                resultElement.style.fontSize = "1.5rem";
                resultElement.style.color = "var(--text-muted)";
            }
        })
        .catch(err => {
            resultElement.innerText = "Error";
            console.error(err);
        });
}
