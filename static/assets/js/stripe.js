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

form.addEventListener('submit', function (event) {
  event.preventDefault()
  card.update({ disabled: true })
  document.querySelector('#submit-button').disabled = true
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: { card: card },
    })
    .then(function (result) {
      if (result.error) {
        const displayError = document.getElementById('card-errors')
        displayError.textContent = result.error.message
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          form.submit()
          document.querySelector('#submit-button').disabled = false
        }
      }
    })
})
