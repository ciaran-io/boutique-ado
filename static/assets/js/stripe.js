const stripePublicKey = document
  .querySelector('#stripe_public_key')
  .textContent.slice(1, -1)
const clientSecret = document
  .querySelector('#client_secret')
  .textContent.slice(1, -1)
let stripe = Stripe(stripePublicKey)
let elements = stripe.elements()
const cardEl = document.querySelector('#card-element')
const form = document.querySelector('#payment-form')

const style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4',
    },
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a',
  },
}
const card = elements.create('card', { style: style })
card.mount(cardEl) // mouth method from stripe.js

card.addEventListener('change', function (event) {
  const displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message
  } else {
    displayError.textContent = ''
  }
})

form.addEventListener('submit', async function (event) {
  event.preventDefault()
  card.update({ disabled: true })
  document.querySelector('#submit-button').disabled = true

  const saveInfo = Boolean(document.querySelector('#id-save-info').checked)
  const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value
  const postData = {
    csrfmiddlewaretoken: csrfToken,
    client_secret: clientSecret,
    save_info: saveInfo,
  }

  const url = '/checkout/cache_checkout_data/'

  const billingDetails = {
    name: form.full_name.value.trim(),
    phone: form.phone_number.value.trim(),
    email: form.email.value.trim(),
    address: {
      line1: form.street_address1.value.trim(),
      line2: form.street_address2.value.trim(),
      city: form.town_or_city.value.trim(),
      country: form.country.value.trim(),
      state: form.county.value.trim(),
    },
  }

  const shippingDetails = {
    name: form.full_name.value.trim(),
    phone: form.phone_number.value.trim(),
    address: {
      line1: form.street_address1.value.trim(),
      line2: form.street_address2.value.trim(),
      city: form.town_or_city.value.trim(),
      country: form.country.value.trim(),
      postal_code: form.postcode.value.trim(),
      state: form.county.value.trim(),
    },
  }

  try {
    await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(postData),
    }).then(() => {
      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
            billing_details: billingDetails,
          },
          shipping: shippingDetails,
        })
        .then((result) => {
          if (result.error) {
            const displayError = document.getElementById('card-errors')
            displayError.textContent = result.error.message
            card.update({ disabled: false })
            document.querySelector('#submit-button').disabled = false
          } else {
            if (result.paymentIntent.status === 'succeeded') {
              document.querySelector('#submit-button').disabled = false
              form.submit()
            }
          }
        })
    })
  } catch (error) {
    console.log(
      'There has been a problem with your fetch operation: ',
      error.message
    )
    location.reload()
  }
})
