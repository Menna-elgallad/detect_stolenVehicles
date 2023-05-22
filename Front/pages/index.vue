<template>
  <div>
    <input type="file" id="file" @change="handleFileUpload" />
    <label for="file" class="btn-2">upload</label>

    <div class="box" v-if="file" style="    margin-bottom: 26px;">
      <span>{{ file.name }}</span>
      <button @click="submitImage" class="detect">Detect</button>
    </div>
    <div>
      <icon name="svg-spinners:8-dots-rotate" class="icon" v-if="showspinner"></icon>
      <div class="dataa mycontainer" v-if="data">
        <div class="img" style="width:50%">
          <img :src="'data:image/jpg;base64,'+detectedImage" style="width:100%" />
        </div>
        <div class="text">
          <p>plate number : {{ carplate }}</p>
          <p v-if="car_location==='not found in our cameras'">Car not fount in our Cameras</p>
          <p v-else>car last seen in {{ car_location }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const file = ref(null);
const detectedImage = ref(null);
const car_location = ref("");
const carplate = ref();
const handleFileUpload = event => {
  file.value = event.target.files[0];
  console.log(file.value);
};
const data = ref();
const showspinner = ref(false);
const submitImage = async () => {
  showspinner.value = true;
  const formData = new FormData();
  formData.append("image", file.value);

  try {
    const response = await fetch("http://localhost:5000/detect", {
      method: "POST",
      body: formData
    });
    data.value = await response.json();
    showspinner.value = false;
    console.log("respnse", data.value);
    // const blob = await response.blob();
    car_location.value = data.value.car_location;
    carplate.value = data.value.plate;
    console.log(data.response);
    detectedImage.value = data.value.response;
  } catch (error) {
    console.error("Error:", error);
  }
};
</script>

<style lang="scss">
[type="file"] {
  height: 0;
  overflow: hidden;
  width: 0;
}

[type="file"] + label {
  background: #f15d22;
  border: none;
  border-radius: 5px;
  color: #fff;
  cursor: pointer;
  display: inline-block;
  font-family: "Rubik", sans-serif;
  font-size: inherit;
  font-weight: 500;
  margin-bottom: 1rem;
  outline: none;
  padding: 1rem 50px;
  position: relative;
  transition: all 0.3s;
  vertical-align: middle;

  &:hover {
    background-color: darken(#f15d22, 10%);
  }

  &.btn-1 {
    background-color: #f79159;
    box-shadow: 0 6px darken(#f79159, 10%);
    transition: none;

    &:hover {
      box-shadow: 0 4px darken(#f79159, 10%);
      top: 2px;
    }
  }

  &.btn-2 {
    background-color: #99c793;
    border-radius: 50px;
    overflow: hidden;

    &::before {
      color: #fff;
      content: "\f382";
      font-family: "Font Awesome 5 Pro";
      font-size: 100%;
      height: 100%;
      right: 130%;
      line-height: 3.3;
      position: absolute;
      top: 0px;
      transition: all 0.3s;
    }

    &:hover {
      background-color: darken(#99c793, 30%);

      &::before {
        right: 75%;
      }
    }
  }

  &.btn-3 {
    background-color: #ee6d9e;
    border-radius: 0;
    overflow: hidden;

    span {
      display: inline-block;
      height: 100%;
      transition: all 0.3s;
      width: 100%;
    }

    &::before {
      color: #fff;
      content: "\f382";
      font-family: "Font Awesome 5 Pro";
      font-size: 130%;
      height: 100%;
      left: 0;
      line-height: 2.6;
      position: absolute;
      top: -180%;
      transition: all 0.3s;
      width: 100%;
    }

    &:hover {
      background-color: darken(#ee6d9e, 30%);

      span {
        transform: translateY(300%);
      }

      &::before {
        top: 0;
      }
    }
  }
}

// Demo specific styles below
body {
  font-family: "Literata", serif;
  font-size: 18px;
  line-height: 1.3;
  margin: 1rem 0;
  text-align: center;
}

.wrapper {
  background-color: #fff;
  border-radius: 1rem;
  margin: 0 auto;
  max-width: 500px;
  padding: 2rem;
  width: 100%;
}

.footer {
  font-size: 0.8rem;
  margin-bottom: 0;
  margin-top: 3rem;
}

h1,
p {
  margin-bottom: 2rem;
}

h1 {
  font-family: "Rubik", sans-serif;
  font-size: 1.7rem;
}

a {
  color: #31c1ef;
  text-decoration: none;
}
.mycontainer {
  width: 80%;
  margin: auto;
  box-shadow: 0 0 8px 2px #ccc;
  border-radius: 1.2rem;
  padding: 1rem;
  display: flex;
  gap: 10px;
  /* border: 1px solid #ccc; */
}
.detect {
  padding: 0.5rem 1rem;
  border-radius: 1.2rem;
  background: none;
  border: 1px solid #ccc;
  margin: 6px 30px;
}
.icon {
  font-size: 100px;
  color: #99c793;
}
.text {
  width: fit-content;
  height: fit-content;
  margin: auto;
}
</style>