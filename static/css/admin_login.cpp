/* admin_login.css */

.admin-login-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 40px 30px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  transition: transform 0.3s ease;
}

.admin-login-container:hover {
  transform: translateY(-5px);
}

.admin-login-container h3 {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 1px;
  font-size: 28px;
  user-select: none;
}

.form-label {
  font-weight: 600;
  color: #34495e;
  display: block;
  margin-bottom: 6px;
  font-size: 1rem;
}

.form-control {
  width: 100%;
  border-radius: 8px;
  border: 1.5px solid #ced4da;
  padding: 12px 15px;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  box-sizing: border-box;
}

.form-control:focus {
  border-color: #1d9bf0;
  box-shadow: 0 0 8px #1d9bf0aa;
  outline: none;
}

.btn-primary {
  background-color: #1d9bf0;
  border: none;
  width: 100%;
  padding: 14px;
  font-weight: 700;
  font-size: 1.1rem;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  margin-top: 15px;
}

.btn-primary:hover,
.btn-primary:focus {
  background-color: #157fc4;
  box-shadow: 0 4px 15px rgba(21, 127, 196, 0.6);
  outline: none;
}

/* Responsive: smaller padding & font sizes on mobile */
@media (max-width: 480px) {
  .admin-login-container {
    margin: 30px 15px;
    padding: 30px 20px;
  }

  .admin-login-container h3 {
    font-size: 24px;
  }

  .form-control {
    padding: 10px 12px;
    font-size: 0.95rem;
  }

  .btn-primary {
    padding: 12px;
    font-size: 1rem;
  }
}
