class Email {
  //value describes the likelihood that the email is related to a job application
    constructor(subject,sender,snippet,date, value) {
      this.snipper = snippet;
      this.subject = subject;
      this.sender = sender
      this.date = date;
      this.value = value;
    }
  
    // Getter methods
    getSubject() {
      return this.subject;
    }
  
    getSender() {
      return this.sender;
    }
  
    getSnippet() {
      return this.snippet;
    }

    getDate() {
      return this.date;
    }
    getValue() {
      return this.value;
    }
  }
  
  export default Email;