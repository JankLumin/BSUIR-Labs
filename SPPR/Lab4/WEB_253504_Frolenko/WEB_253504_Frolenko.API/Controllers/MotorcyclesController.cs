using Microsoft.AspNetCore.Mvc;
using WEB_253504_Frolenko.API.Services.MotorcycleService;
using WEB_253504_Frolenko.Domain.Entities;
using WEB_253504_Frolenko.Domain.Models;

namespace WEB_253504_Frolenko.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MotorcyclesController : ControllerBase
    {
        private readonly IMotorcycleService _motorcycleService;

        public MotorcyclesController(IMotorcycleService motorcycleService)
        {
            _motorcycleService = motorcycleService;
        }

        [HttpGet("categories/{categoryName?}")]
        public async Task<ActionResult<ResponseData<List<Motorcycle>>>> GetMotorcycles(string? categoryName, int pageNo = 1, int pageSize = 3)
        {
            var result = await _motorcycleService.GetProductListAsync(categoryName, pageNo, pageSize);
            return Ok(result);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ResponseData<Motorcycle>>> GetMotorcycle(int id)
        {
            var result = await _motorcycleService.GetProductByIdAsync(id);
            if (!result.Successfull || result.Data == null)
            {
                return NotFound(result.ErrorMessage);
            }
            return Ok(result);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> PutMotorcycle(int id, Motorcycle motorcycle)
        {
            if (id != motorcycle.Id)
            {
                return BadRequest("Motorcycle ID mismatch.");
            }

            await _motorcycleService.UpdateProductAsync(id, motorcycle);
            return NoContent();
        }

        [HttpPost]
        public async Task<ActionResult<ResponseData<Motorcycle>>> PostMotorcycle(Motorcycle motorcycle)
        {
            var result = await _motorcycleService.CreateProductAsync(motorcycle);
            return CreatedAtAction(nameof(GetMotorcycle), new { id = result.Data.Id }, result);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteMotorcycle(int id)
        {
            await _motorcycleService.DeleteProductAsync(id);
            return NoContent();
        }
    }
}
