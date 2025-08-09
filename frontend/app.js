const API = 'http://127.0.0.1:8000';

async function fetchProducts(e) {
  if (e) e.preventDefault();
  const search = document.getElementById('search').value;
  const min_price = document.getElementById('min_price').value;
  const max_price = document.getElementById('max_price').value;
  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (min_price) params.append('min_price', min_price);
  if (max_price) params.append('max_price', max_price);

  const res = await fetch(`${API}/products?` + params.toString());
  const data = await res.json();
  const div = document.getElementById('products');
  div.innerHTML = '<ul>' + data.map(p => `<li>#${p.id} ${p.name} — $${p.price} (stock ${p.stock_qty})</li>`).join('') + '</ul>';
}

async function addProduct(e) {
  e.preventDefault();
  const payload = {
    name: document.getElementById('p_name').value,
    description: document.getElementById('p_desc').value,
    price: parseFloat(document.getElementById('p_price').value),
    stock_qty: parseInt(document.getElementById('p_stock').value, 10)
  };
  const res = await fetch(`${API}/products`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (res.ok) {
    document.getElementById('addProductMsg').textContent = 'Product added ✔';
    fetchProducts();
  } else {
    const err = await res.json();
    document.getElementById('addProductMsg').textContent = 'Error: ' + err.detail;
  }
}

async function addCustomer(e) {
  e.preventDefault();
  const payload = {
    name: document.getElementById('c_name').value,
    email: document.getElementById('c_email').value,
  };
  const res = await fetch(`${API}/customers`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (res.ok) {
    const data = await res.json();
    document.getElementById('addCustomerMsg').textContent = `Customer #${data.id} created ✔`;
  } else {
    const err = await res.json();
    document.getElementById('addCustomerMsg').textContent = 'Error: ' + err.detail;
  }
}

async function createPurchase(e) {
  e.preventDefault();
  const cid = parseInt(document.getElementById('cust_id').value, 10);
  let items;
  try {
    items = JSON.parse(document.getElementById('items_json').value);
  } catch (e) {
    document.getElementById('purchaseMsg').textContent = 'Invalid JSON';
    return;
  }
  const payload = { customer_id: cid, items };
  const res = await fetch(`${API}/purchases`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  const div = document.getElementById('purchaseMsg');
  if (res.ok) {
    const data = await res.json();
    div.textContent = `Purchase #${data.id} created: $${data.total_amount}`;
    fetchProducts();
  } else {
    const err = await res.json();
    div.textContent = 'Error: ' + err.detail;
  }
}

async function fetchLowStock(e) {
  e.preventDefault();
  const threshold = document.getElementById('low_threshold').value;
  const params = new URLSearchParams();
  if (threshold) params.append('threshold', threshold);
  const res = await fetch(`${API}/products/low_stock?` + params.toString());
  const data = await res.json();
  const div = document.getElementById('lowStock');
  if (!data.length) {
    div.textContent = 'No low-stock products';
    return;
  }
  div.innerHTML = '<ul>' + data.map(p => `<li>#${p.id} ${p.name} — stock ${p.stock_qty}</li>`).join('') + '</ul>';
}

async function updateProduct(e) {
  e.preventDefault();
  const id = parseInt(document.getElementById('u_id').value, 10);
  const name = document.getElementById('u_name').value.trim();
  const description = document.getElementById('u_desc').value.trim();
  const priceStr = document.getElementById('u_price').value;
  const stockStr = document.getElementById('u_stock').value;
  const payload = {};
  if (name) payload.name = name;
  if (description) payload.description = description;
  if (priceStr !== '') {
    const price = parseFloat(priceStr);
    if (!isNaN(price)) payload.price = price;
  }
  if (stockStr !== '') {
    const stock = parseInt(stockStr, 10);
    if (!isNaN(stock)) payload.stock_qty = stock;
  }
  if (Object.keys(payload).length === 0) {
    document.getElementById('updateProductMsg').textContent = 'Provide at least one field to update';
    return;
  }
  const res = await fetch(`${API}/products/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  const div = document.getElementById('updateProductMsg');
  if (res.ok) {
    div.textContent = `Product #${id} updated ✔`;
    fetchProducts();
  } else {
    const err = await res.json();
    div.textContent = 'Error: ' + err.detail;
  }
}

async function toggleActive(e) {
  e.preventDefault();
  const id = parseInt(document.getElementById('a_id').value, 10);
  const active = document.getElementById('a_active').checked;
  const res = await fetch(`${API}/products/${id}/active`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ active }) });
  const div = document.getElementById('toggleActiveMsg');
  if (res.ok) {
    div.textContent = `Product #${id} active=${active} ✔`;
    fetchProducts();
  } else {
    const err = await res.json();
    div.textContent = 'Error: ' + err.detail;
  }
}

async function fetchPurchaseDetail(e) {
  e.preventDefault();
  const id = parseInt(document.getElementById('p_id').value, 10);
  const res = await fetch(`${API}/purchases/${id}`);
  const div = document.getElementById('purchaseDetail');
  if (res.ok) {
    const data = await res.json();
    const items = data.items || [];
    const itemsHtml = items.length ? ('<ul>' + items.map(it => `<li>${it.product_name}: ${it.qty} × $${it.unit_price}</li>`).join('') + '</ul>') : '<em>No items</em>';
    div.innerHTML = `
      <p>#${data.id} — customer ${data.customer_id} — ${new Date(data.purchased_at).toLocaleString()}</p>
      <p>Total: $${data.total_amount} — Status: ${data.status}</p>
      <h4>Items</h4>
      ${itemsHtml}
    `;
  } else {
    const err = await res.json();
    div.textContent = 'Error: ' + err.detail;
  }
}

document.getElementById('searchForm').addEventListener('submit', fetchProducts);
document.getElementById('addProductForm').addEventListener('submit', addProduct);
document.getElementById('addCustomerForm').addEventListener('submit', addCustomer);
document.getElementById('purchaseForm').addEventListener('submit', createPurchase);
document.getElementById('lowStockForm').addEventListener('submit', fetchLowStock);
document.getElementById('updateProductForm').addEventListener('submit', updateProduct);
document.getElementById('toggleActiveForm').addEventListener('submit', toggleActive);
document.getElementById('purchaseDetailForm').addEventListener('submit', fetchPurchaseDetail);

fetchProducts();
