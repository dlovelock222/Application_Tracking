class UserAuthentication {
  constructor() {
    this.isLoggedIn = false;
    this.userDetails = null;
  }

  login(id,name,email) {
    this.isLoggedIn = true;
    this.userDetails = {
      id: id,
      name: name,
      email:email,
    };
  }

  logout() {
    this.isLoggedIn = false;
    this.userDetails = null;
  }

  getUserDetails() {
    return this.userDetails;
  }

  isUserLoggedIn() {
    return this.isLoggedIn;
  }
}

// Creating a singleton instance of UserAuthentication
const userAuthInstance = new UserAuthentication();

// Export the singleton instance to use it throughout your application
export default userAuthInstance;