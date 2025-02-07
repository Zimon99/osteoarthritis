<template>
  <div class="register">
    <div class="container mt-5">
      <div class="header">
        <button
          v-if="currentStep > 1"
          class="back-button"
          @click="goToPreviousStep"
        >
          <img src="@/assets/back-icon.svg" alt="Indietro" class="back-icon" />
        </button>
      </div>

      <span class="step-title">Passaggio {{ currentStep }} di 4</span>
      <h2 class="mb-4">Crea un Account</h2>

      <form @submit.prevent="onSubmit">
        <!-- Step 1: Dati Anagrafici -->
        <div v-if="currentStep === 1">
          <div class="mb-3">
            <label for="nome" class="form-label">Nome</label>
            <input
              id="nome"
              v-model="form.nome"
              type="text"
              class="form-control"
              style="text-transform: uppercase"
              required
            />
          </div>

          <div class="mb-3">
            <label for="cognome" class="form-label">Cognome</label>
            <input
              id="cognome"
              v-model="form.cognome"
              type="text"
              class="form-control"
              style="text-transform: uppercase"
              required
            />
          </div>

          <div class="mb-3">
            <label for="gender" class="form-label">Genere</label>
            <select
              id="gender"
              v-model="form.gender"
              class="form-control"
              required
            >
              <option value="Male">MASCHIO</option>
              <option value="Female">FEMMINA</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="data" class="form-label">Data di Nascita</label>
            <input
              id="data"
              v-model="form.data"
              type="date"
              class="form-control"
              @change="correctDate"
              style="text-transform: uppercase"
              required
            />
          </div>
        </div>

        <!-- Step 2: Dati di Contatto -->
        <div v-if="currentStep === 2">
          <div class="mb-3">
            <label for="address" class="form-label">Indirizzo</label>
            <input
              id="address"
              v-model="form.address"
              type="text"
              class="form-control"
              style="text-transform: uppercase"
              required
              placeholder="(es. Via Roma 1)"
            />
          </div>

          <div class="mb-3">
            <label for="cap_code" class="form-label">CAP</label>
            <input
              id="cap_code"
              v-model="form.cap_code"
              type="number"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label for="tax_code" class="form-label">Codice Fiscale</label>
            <input
              id="tax_code"
              v-model="form.tax_code"
              type="text"
              class="form-control"
              style="text-transform: uppercase"
              required
            />
          </div>

          <div class="mb-3">
            <label for="telefono" class="form-label">Numero di Telefono</label>
            <input
              id="telefono"
              v-model="form.telefono"
              type="tel"
              class="form-control"
              required
              placeholder="(es. +391234567890)"
            />
          </div>
        </div>

        <!-- Step 3: Credenziali -->
        <div v-if="currentStep === 3">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label"
              >Password
              <span
                class="info-icon"
                title="Requisiti per la password: min 8 caratteri, almeno una maiuscola, una minuscola un numero e un carattere speciale."
              >
                <img
                  src="@/assets/info-icon.svg"
                  alt="Info"
                  class="info-image"
                />
              </span>
            </label>
            <div class="input-group">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-control password-input"
                :class="{
                  'is-invalid': !isPasswordValid && passwordInputTouched,
                }"
                required
                @input="passwordInputTouched = true"
                @paste.prevent
              />
              <button
                type="button"
                class="btn eye-button"
                @click="toggleShowPassword"
              >
                <img
                  :src="
                    showPassword
                      ? require('@/assets/eye-off.svg')
                      : require('@/assets/eye-on.svg')
                  "
                  alt="Toggle Password Visibility"
                  class="eye-icon"
                />
              </button>
            </div>
            <div
              v-if="passwordInputTouched && !isPasswordValid"
              class="text-danger mt-1"
            >
              La password deve contenere almeno: un numero, una lettera
              maiuscola, una lettera minuscola e un carattere speciale ed essere
              lunga almeno 8 caratteri.
            </div>
          </div>

          <div class="mb-3">
            <label for="confirmPassword" class="form-label"
              >Conferma Password</label
            >
            <div class="input-group">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-control password-input"
                :class="{ 'is-invalid': showPasswordError }"
                required
                @input="confirmPasswordTouched = true"
                @paste.prevent
              />
              <button
                type="button"
                class="btn eye-button"
                @click="toggleShowConfirmPassword"
              >
                <img
                  :src="
                    showConfirmPassword
                      ? require('@/assets/eye-off.svg')
                      : require('@/assets/eye-on.svg')
                  "
                  alt="Toggle Password Visibility"
                  class="eye-icon"
                />
              </button>
            </div>
            <div
              v-if="
                confirmPasswordTouched && form.password !== form.confirmPassword
              "
              class="text-danger mt-1"
            >
              Le password non corrispondono.
            </div>
          </div>
        </div>

        <!-- Bottone di avanzamento o submit -->
        <div v-if="currentStep < 3">
          <button
            type="button"
            class="btn btn-primary btn-next"
            :disabled="!isStepValid(currentStep)"
            @click="goToNextStep"
            @mouseover="isHover = true"
            @mouseleave="isHover = false"
            @mouseenter="showDisabledIcon = !isStepValid(currentStep)"
          >
            Avanti
            <span
              v-if="!isStepValid(currentStep) && isHover"
              class="disabled-icon"
            >
              <img
                src="@/assets/prohibition-icon.svg"
                alt="Non disponibile"
                class="prohibition-icon"
              />
            </span>
          </button>
        </div>

        <!-- Submit button (Step 3) -->
        <div v-if="currentStep === 3">
          <button
            type="submit"
            class="btn btn-primary btn-next"
            :disabled="loading || !isStepValid(currentStep)"
          >
            <span v-if="loading">Registrazione...</span>
            <span v-else>Registrati</span>
          </button>

          <!-- Error message -->
          <div v-if="errors.general" class="invalid-feedback mt-3">
            {{ errors.general }}
          </div>
        </div>

        <div v-if="currentStep === 4">
          <p>{{ successMessage }}</p>
          <button class="btn btn-primary btn-next" @click="goToHome">
            Torna alla home
          </button>
        </div>
      </form>
    </div>

    <!-- Loading overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-icon">
        <img src="@/assets/loading-icon.svg" alt="Loading..." />
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

  export default {
    data() {
      return {
        currentStep: 1,
        loading: false,
        showPassword: false,
        showConfirmPassword: false,
        errors: {},
        form: {
          nome: "",
          cognome: "",
          gender: "",
          data: "",
          address: "",
          cap_code: "",
          tax_code: "",
          telefono: "",
          username: "",
          email: "",
          password: "",
          confirmPassword: "",
        },
      };
    },
    computed: {
      // Computed property per la validazione della password
      isPasswordValid() {
        const password = this.form.password || "";
        const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
        return regex.test(password);
      },
    },
    methods: {
      goToHome() {
        this.currentStep = 1;
        this.form = {
          nome: "",
          cognome: "",
          gender: "",
          data: "",
          address: "",
          cap_code: "",
          tax_code: "",
          telefono: "",
          username: "",
          email: "",
          password: "",
          confirmPassword: "",
        };

        this.$router.push("/welcome");
      },
      correctDate() {
        const dateParts = this.form.data.split("-");
        const year = parseInt(dateParts[0], 10);
        const month = parseInt(dateParts[1], 10);
        const day = parseInt(dateParts[2], 10);

        // Correzione dell'anno
        if (year >= 3000) {
          dateParts[0] = "2006";
        } else if (year === 0) {
          dateParts[0] = "1900";
        }

        // Correzione del mese
        if (month > 12) {
          dateParts[1] = "12";
        }

        // Correzione del giorno
        if (day > 31) {
          dateParts[2] = "31";
        }

        // Imposta la data corretta
        this.form.data = dateParts.join("-");
      },
      goToNextStep() {
        if (this.currentStep < 4) {
          this.currentStep++;
        }
      },
      goToPreviousStep() {
        if (this.currentStep > 1) {
          this.currentStep--;
        }
      },
      toggleShowPassword() {
        this.showPassword = !this.showPassword;
      },
      toggleShowConfirmPassword() {
        this.showConfirmPassword = !this.showConfirmPassword;
      },
      async onSubmit() {
        this.loading = true;
        this.errors = {};

        try {
            const { email, password, ...userData } = this.form;

            const response = await axios.post("http://127.0.0.1:5000/register", {
                email: email,
                password: password,  // Invio della password al backend
                nome: userData.nome,
                cognome: userData.cognome,
                gender: userData.gender,
                data: userData.data,
                address: userData.address,
                cap_code: userData.cap_code,
                tax_code: userData.tax_code,
                telefono: userData.telefono,
                username: userData.username,
            });

            // Log di debug: risposta dal backend
            console.log("Response dal backend:", response.data);

            // Reset form e mostra messaggio di successo
            this.successMessage = "Registrazione completata con successo!";
            this.loading = false;
            this.currentStep = 4;

        } catch (error) {
            console.error("Errore nella registrazione:", error);
            this.errors.general = error.message;
            this.loading = false;
        }
        },
        isStepValid(step) {
          if (step === 1) {
            return (
              this.form.nome &&
              this.form.cognome &&
              this.form.gender &&
              this.form.data
            );
          } else if (step === 2) {
            return (
              this.form.address &&
              this.form.cap_code &&
              this.form.tax_code &&
              this.form.telefono
            );
          } else if (step === 3) {
            return (
              this.form.username &&
              this.form.email &&
              this.isPasswordValid &&
              this.confirmPasswordTouched &&  // Verifica che l'utente abbia toccato il campo di conferma password
              this.form.password === this.form.confirmPassword
            );
          }
          return false;
        },
    },
  };
</script>




<style scoped>
.register {
  background: #ffffff; /* Sfondo bianco */
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0px 0px rgba(0, 0, 0, 0);
}

.container {
  max-width: 400px;
  padding: 40px;
  border-radius: 15px;
  background: #ffffff;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  margin-top: 100px;
  height: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-button {
  background: transparent;
  border: none;
  cursor: pointer;
  margin-left: -10px;
}

.back-icon {
  width: 30px;
  height: 30px;
}

.step-title {
  font-size: 10px;
  margin-bottom: 10px;
}

h2 {
  font-size: 18px;
  margin-bottom: 30px;
}

.form-label {
  font-size: 12px;
}

.form-control {
  background: #f2f2f2;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 12px;
}

.input-group {
  position: relative;
}

.text-danger {
  font-size: 0.8rem; /* Font più piccolo (puoi modificarlo a piacere) */
}

.eye-button {
  background: transparent;
  border: 1px solid #ccc;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  width: 46px;
}

.eye-icon {
  width: 18px;
  height: 18px;
  margin: auto;
}

.info-icon {
  margin-left: 5px;
  display: inline-block;
  font-size: 12px;
}

.info-image {
  width: 15px;
  height: 15px;
  vertical-align: middle;
}

.btn-next {
  width: 100%;
  margin-top: 15px;
  padding: 0.4rem;
  cursor: pointer;
  font-size: 13px; /* Dimensione del testo più piccola */
}

.btn-next {
  font-size: 13px; /* Dimensione del testo più piccola per il pulsante "Avanti" */
}

.btn-next:hover {
  background-color: #c0c0c0;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-icon {
  width: 50px;
}

.disabled-icon {
  margin-left: 10px;
}

.prohibition-icon {
  width: 16px;
  height: 16px;
  vertical-align: middle;
  display: inline-block;
}
</style>
