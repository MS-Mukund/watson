import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';
import { useSnackbar } from 'notistack'; // For snackbar notifications

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
  formControl: {
    minWidth: 120,
  },
}));

const options = [
  { value: 'option1', label: 'Option 1' },
  { value: 'option2', label: 'Option 2' },
  // ... Add more options
];

function MyForm() {
  const classes = useStyles();
  const { enqueueSnackbar } = useSnackbar(); // Snackbar instance

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    dropdownValue: 'option1', // Set default selected value
    image: null,
  });

  const handleChange = (event) => {
    const { name, value, files } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value === 'image' ? files[0] : value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const { name, dropdownValue, image } = formData;

    // Form validation (optional, customize as needed)
    if (!name || !image) {
      enqueueSnackbar('Please fill out all required fields.', { variant: 'error' });
      return;
    }

    // Handle form submission (e.g., send data to backend)
    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('dropdownValue', dropdownValue);
    formData.append('image', image);

    fetch('/your-backend-endpoint', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        enqueueSnackbar('Form submitted successfully!', { variant: 'success' });
        // Handle successful submission (e.g., reset form)
        setFormData({ name: '', email: '', dropdownValue: 'option1', image: null });
      })
      .catch((error) => {
        enqueueSnackbar('Error submitting form.', { variant: 'error' });
        console.error(error);
      });
  };

  return (
    <form className={classes.root} onSubmit={handleSubmit}>
      <TextField
        label="Name"
        name="name"
        value={formData.name}
        onChange={handleChange}
      />
      <TextField
        label="Email"
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
      />
      <FormControl className={classes.formControl}>
        <InputLabel id="dropdown-label">Dropdown</InputLabel>
        <Select
          labelId="dropdown-label"
          id="dropdown"
          value={formData.dropdownValue}
          onChange={handleChange}
          label="Dropdown"
        >
          {options.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <input
        accept="image/*"
        id="image-upload"
        type="file"
        name="image"
        onChange={handleChange}
        hidden
      />
      <label htmlFor="image-upload">
        <Button variant="contained" component="span">
          Upload Image
        </Button>
      </label>
      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </form>
  )};

export default MyForm;
