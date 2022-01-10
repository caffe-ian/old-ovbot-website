function initPayPalButton() {
        var itemOptions = document.querySelector("#smart-button-container #item-options");
    var quantity = parseInt(20);
    var quantitySelect = document.querySelector("#smart-button-container #quantitySelect");
    var priceTotal;
    if (!isNaN(quantity)) {
      quantitySelect.style.visibility = "visible";
    }
    var orderDescription = 'OV Bot';
    if(orderDescription === '') {
      orderDescription = 'Item';
    }
    paypal.Buttons({
      style: {
        shape: 'rect',
        color: 'gold',
        layout: 'vertical',
        label: 'paypal',
        
      },
      createOrder: function(data, actions) {
        var selectedItemDescription = itemOptions.options[itemOptions.selectedIndex].value;
        let _prices = {
            "Donator Case": 1.99,
            "Donator Pack": 4.99,
            "Pro Pack": 9.99,
            "Hacker Pack": 19.99,
        }
        var selectedItemPrice = _prices[selectedItemDescription]

        var tax = (0 === 0 || false) ? 0 : (selectedItemPrice * (parseFloat(0)/100));
        if(quantitySelect.options.length > 0) {
          quantity = parseInt(quantitySelect.options[quantitySelect.selectedIndex].value);
        } else {
          quantity = 1;
        }

        tax *= quantity;
        tax = Math.round(tax * 100) / 100;
        priceTotal = quantity * selectedItemPrice + tax;
        priceTotal = Math.round(priceTotal * 100) / 100;
        var itemTotalValue = Math.round((selectedItemPrice * quantity) * 100) / 100;

        return actions.order.create({
          purchase_units: [{
            description: orderDescription,
            amount: {
              currency_code: 'USD',
              value: priceTotal,
              breakdown: {
                item_total: {
                  currency_code: 'USD',
                  value: itemTotalValue,
                },
                tax_total: {
                  currency_code: 'USD',
                  value: tax,
                }
              }
            },
            items: [{
              name: selectedItemDescription,
              unit_amount: {
                currency_code: 'USD',
                value: selectedItemPrice,
              },
              quantity: quantity
            }]
          }],
          application_context: {
              shipping_preference: 'NO_SHIPPING'
            }
        });
      },
      onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
          success = details['status']
          pu = details['purchase_units']
          a = pu['0']
          items = a['items']
          b = items['0']
          itemname = b['name']
          quantity = b['quantity']
          var data = {'price': priceTotal, 'success': success, 'itemname': itemname, 'quantity': quantity, 'userid': '{{ userid }}', 'username': '{{ username }}', 'csrfmiddlewaretoken': '{{ csrf_token }}', 'gift': "True", 'gifterid': '{{gifterid}}', 'giftername': '{{giftername}}' };
          $.post("../purchase-success/", data);
          setTimeout(() => {  window.location.replace("../purchase-success/"); }, 1000);
        });
      },
      onError: function(err) {
        window.location.replace("../purchase-fail");
      },
      onCancel: function(data) {
        alert("Transaction cancelled.")
      },
    }).render('#paypal-button-container');
  }
  initPayPalButton();
