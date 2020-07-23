import React, { Component } from "react"

class Search extends Component {
  state = {
    query: "",
    query_page: 1,
  }

  getInfo = (event) => {
    event.preventDefault()
    this.props.submitSearch(this.state.query, this.state.query_page)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value,
    })
  }

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input placeholder="Search questions..." ref={(input) => (this.search = input)} onChange={this.handleInputChange} />
        <input type="submit" value="Submit" className="button" />
      </form>
    )
  }
}

export default Search
