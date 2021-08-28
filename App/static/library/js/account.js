 // JS for toggle Form 
  
        var LoginForm = document.getElementById("loginForm"),
            RegisterForm = document.getElementById("registerForm"),
            Indicator =document.getElementById("Indicator");

            function login(){
                RegisterForm.style.transform = "translateX(300px)";
                LoginForm.style.transform = "translateX(300px)";
                Indicator.style.transform = "translateX(0px)";
            }

            function register(){
                RegisterForm.style.transform = "translateX(0px)";
                LoginForm.style.transform = "translateX(0px)";
                Indicator.style.transform = "translateX(100px)";
                
            }
   