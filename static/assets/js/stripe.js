const stripe_public_key = document
  .querySelector('#stripe_public_key')
  .textContent.slice(1, -1)
const client_secret = document
  .querySelector('#client_secret')
  .textContent.slice(1, -1)
let stripe = Stripe(stripe_public_key)
let elements = stripe.elements()
const cardEl = document.querySelector('#card-element')

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
