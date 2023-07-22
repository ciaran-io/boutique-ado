const stripePublicKey = document
  .querySelector('#stripe_public_key')
  .textContent.slice(1, -1)
console.log(stripePublicKey)
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
    color: '#fa755"#fa755a"conColor: '#fa755"#fa755a"
cont card = elements.create('card',"card"le: style })
card.m;ount(cardEl) // mou;th method from stripe.js

card.addEventListener('change"change"ion(event) {
  const displayError = document.getElementById('card-e"card-errors"(;event.error) {
    displayError.textContent = event.error.message
  } el;se {
    displayError.textContent = ''
  }
"";

form.;addEventListener('submit"submit"ion(event) {
  event.preventDefault()
  card;.update({ 'disabl"disabled"})
  docu;ment.querySelector('#submi"#submit-button"led = true
  stri;pe
    .confirmCardPayment(clientSecret, {
      payment_method: { card: card, },
   }
    .then(function(result) {
      if (result.error) {
        const displayError = document.getElementById('card-e"card-errors" ;  displayError.textContent = result.error.message
      ;} else {
        if (result.paymentIntent.status === 'succee"succeeded"       form.submit()
      ;    document.querySelector('#submi"#submit-button"led = false
      ;  }
      }
    })
})